import sys
import hashlib
import time
import uuid
import sys
import os
from enum import Enum
from copy import deepcopy
from hashids import Hashids
from sqlalchemy.sql.expression import select, text


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import dataset
import fire
from validate_email import validate_email

from app.config import DB_URL, TESTDB, REWARDS
from app.util import referral_hash, send_simple_message
salt = str("XXX")
hashids = Hashids(salt=salt)

db = dataset.connect(TESTDB, row_type=dict)




    # Loop through the goals (in reverse)
        # Check the goal with the degree
        #   If it's the correct degree
        #   

class StatusCodes(Enum):
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    BADREQ = 400
    UNAUTH = 401
    FORBIDDEN = 403
    NOTFOUND = 404
    MYBAD = 500



# ------------------------------------------------------------
# ------------------ Global Functions ------------------------
# ------------------------------------------------------------

def hash_pass(password):
    password = str(password)
    hashed = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()
    return hashed





def formatting(status, msg, data):
    return {
        "status": status,
        "msg": msg,
        "data": data
    }


def check_referrals(email):
    usertable = db['user_referral']
    utable = usertable.table
    utable_alias = utable.alias()

    lvl1_query = select([
        utable.c.email, 
        utable.c.created_at
    ]).where(
        utable.c.referred_by==email
    )

    l1_alias = lvl1_query.cte().alias()
    l2_query = select([
        utable.c.email, 
        utable.c.created_at
    ]).where(utable_alias.c.referred_by==l1_alias.c.email)
    
    lvl_2_list = []
    lvl_3_list = []
    referred_list_lvl_1 = list(db.query(lvl1_query))
    for l1_user in referred_list_lvl_1:
        l2_query = select([
            utable_alias.c.email, 
            utable_alias.c.created_at
        ]).where(utable_alias.c.referred_by==l1_user["email"])
        l2_referred_list = list(db.query(l2_query))
        for l2_user in l2_referred_list:
            lvl_2_list.append(l2_user)
        
    for l2_user in lvl_2_list:
        l3_query = select([
            utable_alias.c.email, 
            utable_alias.c.created_at
        ]).where(utable_alias.c.referred_by==l2_user["email"])
        l3_referred_list = list(db.query(l3_query))
        for l3_user in l3_referred_list:
            lvl_3_list.append(l3_user)

    first_count = len(referred_list_lvl_1)
    second_count = len(lvl_2_list)
    third_count = len(lvl_3_list)

    return {
        "first": {"count": first_count, "list": referred_list_lvl_1},
        "second": {"count": second_count, "list": lvl_2_list},
        "third": {"count": third_count, "list": lvl_3_list}
    }


class User(object):
    def __init__(self):
        self.userdb = db['user_referral']
        self.infodb = db['user_keyinfo']

    def get_user_info(self, email):
        # Only give information if the user is in the system
        try:
            # Make sure to return 500 if necessary
            is_valid = validate_email(email)

            if is_valid is False:
                return formatting(StatusCodes.BADREQ.value, "Make sure the email is spelled correctly.", {})

            self.current_user(email)
            if self.user is None:
                return formatting(StatusCodes.BADREQ.value, "User Doesn't Exist", {})

            # check_referrals

            referral_info = check_referrals(email)
            
            self.user.pop("password", None)

            return formatting(StatusCodes.OK.value, "Referral Information", {
                "referred": {
                    "l1": {
                        "count": referral_info['first']['count'],
                        "list": referral_info['first']['list']
                    },
                    "l2": {
                        "count": referral_info['second']['count'],
                        "list": referral_info['second']['list']
                    },
                    "l3": {
                        "count": referral_info['third']['count'],
                        "list": referral_info['third']['list']
                    }
                },
                "user": self.user,
                "options": REWARDS
            })
        except Exception as e:
            print(str(e), file=sys.stderr)
            return formatting(StatusCodes.MYBAD.value, "Looks like an unexpected error occured", {})
        
    
    

    def admin_remove(self, email):

        try:
            is_valid = validate_email(email, verify=True)

            if is_valid is False:
                return formatting(StatusCodes.BADREQ.value, "Make sure the email is spelled correctly.", {})
            
            self.current_user(email)
            
            if self.user is None:
                return formatting(StatusCodes.BADREQ.value, "User Doesn't Exist. ", {})

            try:
                self.userdb.delete(email=email)
            except Exception:
                return formatting(StatusCodes.MYBAD.value, "Shit Happened", {})
            return formatting(StatusCodes.OK.value, "Successfully deleted", {})
        except Exception:
            return formatting(StatusCodes.MYBAD.value, "Looks like an unexpected error occured", {})


        

    def current_user(self, email):
        # Set for now
        self.user = None
        self.user = self.userdb.find_one(email=email)
        return self.user


    def login(self, email, password):
        try:
            is_valid = validate_email(email)

            if is_valid is False:
                return formatting(StatusCodes.BADREQ.value, "Make sure the email is spelled correctly.", {})

            self.current_user(email)
            if self.user is None:
                return formatting(StatusCodes.BADREQ.value, "User Doesn't Exist. Try Logging In", {})

            hashed_password = hash_pass(password)
            if hashed_password != self.user['password']:
                return formatting(StatusCodes.UNAUTH.value, "Incorrect credentials", {})
            
            wo_pass = deepcopy(self.user)
            wo_pass.pop('password', None)

            return formatting(StatusCodes.OK.value, "Login Successful", wo_pass)
        except Exception as e:
            print(e, file=sys.stderr)
            return formatting(StatusCodes.MYBAD.value, "Looks like an unexpected error occured", {})
        





    def register(self, email, password, confirm, referrer, first, last, ip):
        try:
            is_valid = validate_email(email)

            if is_valid is False:
                return formatting(StatusCodes.BADREQ.value, "Make sure the email is spelled correctly.", {})


            self.current_user(email)

            if password != confirm:
                return formatting(StatusCodes.BADREQ.value, "Passwords Don't Match", {})
            

            if self.user != None:
                cp_user = deepcopy(self.user)
                cp_user.pop("password", None)
                return formatting(StatusCodes.FORBIDDEN.value, "User Already Exist", cp_user)

            # Check if the password and confirm match
            
            exist_user = self.userdb.find_one(ip=ip)
            print(ip, file=sys.stderr)
            if exist_user is not None:
                return formatting(StatusCodes.BADREQ.value, "Sorry, you can't use the same computer to register twice", {})



            _referrer = None
            referrer_email = None
            if referrer is not None:
                _referrer = self.userdb.find_one(referral_hash=referrer)
                if _referrer is None:
                    referrer_email = None
                else:
                    referrer_email = _referrer['email']



            created_at = time.time()
            hashed_password = hash_pass(password)
            user_hash = referral_hash(email)
            user_info = {
                "email": email,
                "password": hashed_password,
                "referred_by": referrer_email,
                "referral_hash":user_hash,
                "first": first,
                "last": last,
                "ip": ip,
                "created_at": created_at
            }
            try:
                self.userdb.insert(user_info)
                # Check the user's referrals and send email if it's good
            except Exception:
                return formatting(StatusCodes.MYBAD.value, "Looks like something went wrong", {})

            user_info.pop("password", None)
            send_simple_message(email, "Thank You For Pre-Registering To Funguana!", 
                """
                    <h2>Hi {}!</h2>
                    <br />
                    <br />
                    <p>You're getting this because you entered in your email for Funguana's Pre-Register. We wanted to say thank you for entering everything in. When we launch, we will give prizes to people based on the number of people they invited for the prelaunch. Please go to the website: referral.funguaservices.com with your email and password to see your progress.
                    </p>
                    <br /><br />
                    <p>You'll be hearing from us very shortly!</p>
                    <br /><br />
                    <p>Best,</p>
                    <p>Kevin Hill</p>
                    <p>Funguana, CEO</p>
                """.format(first)
            )
            return formatting(StatusCodes.OK.value, "User successfully created", user_info)
        except Exception as e:
            print(e, file=sys.stderr)
            return formatting(StatusCodes.MYBAD.value, "Looks like an unexpected error occured", {})
        

    def add_user_information(self, email, info_type, info):
        """ Should be called inside of python-rq function"""
        is_valid = validate_email(email, verify=True)

        if is_valid is False:
            return formatting(StatusCodes.BADREQ.value, "Make sure the email is spelled correctly.", {})
        

        self.current_user(email)
        
        if self.user is None:
            return formatting(StatusCodes.BADREQ.value, "User Doesn't Exist. Try Logging In", {})

        itype_str = isinstance(info_type, str)
        info_str = isinstance(info, str)

        if info_type not in ['reward', 'cache'] or itype_str is False:
            # Return an error here saying the type isn't correct
            return formatting(StatusCodes.BADREQ.value, "Info type doesn't exist. Try picking reward or cache", {})
        
        if info_str is False:
            return formatting(StatusCodes.BADREQ.value, "Info isn't a string. Shame on you!", {})
        
        # Make sure the email exist
        
        # Add the information
        # Replace spaces with underscores
        info.replace(" ", "_")
        existing_record = self.infodb.find_one(email=email, info=info, type=info_type)

        if existing_record is not None:
            return formatting(StatusCodes.BADREQ.value, "This type of information has been added already", {})
        


        insert_info = {
            "created_at": time.time(),
            "type": info_type,
            "email": email,
            "info": info
        }

        self.infodb.insert(insert_info)

        return formatting(StatusCodes.OK.value, "User info successfully added", insert_info)
        
    def info_by_type(self, email, info_type):
        if info_type not in ['reward', 'cache']:
            # Return an error here saying the type isn't correct
            return formatting(StatusCodes.BADREQ.value, "Info type doesn't exist. Try picking reward or cache", {})
        
        self.infodb.find(email=email, type=info_type)





class DBCli(object):
    def __init__(self):
        """ Use class to Initialize the Database """
        pass
    
    def init_all(self):
        self.init_user()
        self.init_user_info()
    
    def drop_user_referral(self):
        db['user_referral'].drop_table()

    def purge_users(self):
        db['user_referral'].delete()

    def init_user(self):
        user_table = db.create_table("user_referral")
        user_table.create_column('created_at', db.types.float)
        user_table.create_column('referred_by', db.types.text)
        user_table.create_column('referral_hash', db.types.text)
        user_table.create_column('ip', db.types.text)
        user_table.create_column('email', db.types.text)
        user_table.create_column('password', db.types.text)
        user_table.create_column('first', db.types.text)
        user_table.create_column('last', db.types.text)

    def init_user_info(self):
        user_rewards = db.create_table("user_keyinfo")
        # Time the info was created
        user_rewards.create_column('created_at', db.types.float)
        # Type of info (reward|cache)
        user_rewards.create_column('type', db.types.text)
        # This is the user's email
        user_rewards.create_column('email', db.types.text)
        # This is the key information behind the user's information
        user_rewards.create_column('info', db.types.text)
        


if __name__ == "__main__":
    fire.Fire(DBCli)
