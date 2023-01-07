# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python

from flask import Blueprint, render_template, request, flash, redirect,g
from python_http_client.exceptions import HTTPError
import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


email_bp = Blueprint('email_bp', __name__,
    template_folder='templates', static_folder='static')


# @email_bp.before_request
def set_domain():
    g.domain="http://localhost:5000"

# @email_bp.route('/signup_email')
def signup_email(u,establishment_name):
    set_domain()
    
    beginning="<h3>Welcome, we are glad you are joining us!</h3>"
    if u.user_type=="provider":
        beginning+="""Thank you for willing to give students in Ontario the opporunity to experience your culinary arts!<br><br>
            To make your account active, we need to verify your identity. Once you have completed your profile and uploaded your
            inspection report, press the "Submit for Confirmation" button to submit your profile. 
            Once we have confirmed your business, you will receive an email that your account is active and you are
            ready to make your menu on our website."""
    elif u.user_type=="school":
        beginning+=f"""Thank you for giving your students the opportunity to experience a wealth of culinary experience.<br><br>
            To finish make your account active, we need to verify your identity. We will be in touch with the principal of
            {establishment_name} to confirm participation. Once we get confirmation, you will receive an email that your account is 
            active and you can start searching our database of participating restaurants and caterers around your area 
            that meet your needs and availability."""
    elif u.user_type=='parent':
        beginning+=f"""Thank you for giving your child the opportunity to experience a wealth of culinary experience.<br><br>
            Some marketing here how they can search for featured menus and search for restaurants and favourite them to 
            influence the choice their school makes."""
    
    link=False
    button=False
    end=False
    footer=False
    message = Mail(
        from_email='Food For Thought School Lunches <signup@fftsl.ca>',
        to_emails=u.email,
        subject='Welcome to Food for Thought School Lunches program',
        html_content=content_builder(beginning,link,button,end,footer))
        
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        
        flash("Your email has been successfully registered.", "success_bkg")
        if u.user_type=='provider':
            return redirect('/')
        return redirect ('/browsing')
    except HTTPError as e:
        # pylint: disable=no-member
        flash("Something went wrong. Please contact support at help@fftsl.ca","failure_bkg")
        print(e.message)

@email_bp.route('/set_password_email')
def set_password_email():
    set_domain()
    key=request.args['key']
    email=request.args['email']
    # only admin users can access this page
    # I input an email and press send and 
    # it will send the user an email to tell them they have been approved and they can set their password
    beginning="""<h3>Set/Reset password to Food for Thoughts School Lunches program</h3>
        If this is your first time setting your password, congratulations, we have verified your identity! Please click on the link
        below to reset your password. """
    link=g.domain+"/set_password?key=" + key
    button= "Set Password"
    end="This link will expire in 5 days from the date and time of this email."
    footer=False
    
    message = Mail(
        from_email='Food For Thought School Lunches Help <help@fftsl.ca>',
        to_emails=email,
        subject='FFTSL Password Set/Reset',
        html_content=content_builder(beginning,link,button,end,footer))
        
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        
        flash("Instructions to reset your password has been sent to your email. In the meantime, feel free to browse around!", "success_bkg")
        return redirect ('/browsing')
    except HTTPError as e:
        # pylint: disable=no-member
        flash("Something went wrong. Please contact support at help@fftsl.ca","failure_bkg")
        print(e.message)
    
# def admin_password_reset():
    
    


def content_builder(beginning,link,button,end, footer):
    email = ""
    email +=f"""<!doctype html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
            <title>Simple Transactional Email</title>
            <style>
        @media only screen and (max-width: 620px) {{
        table.body h1 {{
            font-size: 28px !important;
            margin-bottom: 10px !important;
        }}

        table.body p,
        table.body ul,
        table.body ol,
        table.body td,
        table.body span,
        table.body a {{
            font-size: 16px !important;
        }}

        table.body .wrapper,
        table.body .article {{
            padding: 10px !important;
        }}

        table.body .content {{
            padding: 0 !important;
        }}

        table.body .container {{
            padding: 0 !important;
            width: 100% !important;
        }}

        table.body .main {{
            border-left-width: 0 !important;
            border-radius: 0 !important;
            border-right-width: 0 !important;
        }}

        table.body .btn table {{
            width: 100% !important;
        }}

        table.body .btn a {{
            width: 100% !important;
        }}

        table.body .img-responsive {{
            height: auto !important;
            max-width: 100% !important;
            width: auto !important;
        }}
        }}
        @media all {{
        .ExternalClass {{
            width: 100%;
        }}

        .ExternalClass,
        .ExternalClass p,
        .ExternalClass span,
        .ExternalClass font,
        .ExternalClass td,
        .ExternalClass div {{
            line-height: 100%;
        }}

        .apple-link a {{
            color: inherit !important;
            font-family: inherit !important;
            font-size: inherit !important;
            font-weight: inherit !important;
            line-height: inherit !important;
            text-decoration: none !important;
        }}

        #MessageViewBody a {{
            color: inherit;
            text-decoration: none;
            font-size: inherit;
            font-family: inherit;
            font-weight: inherit;
            line-height: inherit;
        }}

        .btn-primary table td:hover {{
            background-color: #34495e !important;
        }}

        .btn-primary a:hover {{
            background-color: #34495e !important;
            border-color: #34495e !important;
        }}
        }}
        </style>
        </head>
        <body style="background-color: #f6f6f6; font-family: sans-serif; -webkit-font-smoothing: antialiased; font-size: 14px; line-height: 1.4; margin: 0; padding: 0; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;">
            <span class="preheader" style="color: transparent; display: none; height: 0; max-height: 0; max-width: 0; opacity: 0; overflow: hidden; mso-hide: all; visibility: hidden; width: 0;">Set/Resetting your FFTSL password.</span>
            <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="body" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #f6f6f6; width: 100%;" width="100%" bgcolor="#f6f6f6">
            <tr>
                <td style="font-family: sans-serif; font-size: 14px; vertical-align: top;" valign="top">&nbsp;</td>
                <td class="container" style="font-family: sans-serif; font-size: 14px; vertical-align: top; display: block; max-width: 580px; padding: 10px; width: 580px; margin: 0 auto;" width="580" valign="top">
                <div class="content" style="box-sizing: border-box; display: block; margin: 0 auto; max-width: 580px; padding: 10px;">

                    <!-- START CENTERED WHITE CONTAINER -->
                    <table role="presentation" class="main" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; background: #ffffff; border-radius: 3px; width: 100%;" width="100%">

                    <!-- START MAIN CONTENT AREA -->
                    <tr>
                        <td class="wrapper" style="font-family: sans-serif; font-size: 14px; vertical-align: top; box-sizing: border-box; padding: 20px;" valign="top">
                        <table role="presentation" border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%;" width="100%">
                            <tr>
                            <td style="font-family: sans-serif; font-size: 14px; vertical-align: top;" valign="top">
                                <p style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; margin-bottom: 15px;">{beginning}</p>"""
    if link:
        email +=f"""<table role="presentation" border="0" cellpadding="0" cellspacing="0" class="btn btn-primary" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; width: 100%;" width="100%">
                                <tbody>
                                    <tr>
                                    <td align="left" style="font-family: sans-serif; font-size: 14px; vertical-align: top; padding-bottom: 15px;" valign="top">
                                        <table role="presentation" border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: auto;">
                                        <tbody>
                                            <tr>
                                            <td style="font-family: sans-serif; font-size: 14px; vertical-align: top; border-radius: 5px; text-align: center; background-color: #3498db;" 
                                            valign="top" align="center" bgcolor="#3498db"> <a href="{link}" target="_blank" style="border: solid 1px #3498db; border-radius: 5px; box-sizing: border-box; cursor: pointer; display: inline-block; 
                                            font-size: 14px; font-weight: bold; margin: 0; padding: 12px 25px; text-decoration: none; text-transform: capitalize; background-color: #3498db; border-color: #3498db; color: #ffffff;">
                                            {button}</a> </td>
                                            </tr>
                                        </tbody>
                                        </table>
                                    </td>
                                    </tr>
                                </tbody>
                                </table>"""
    if end:
        email += f"""<p style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; margin-bottom: 15px;">{end}</p>
                            </td>
                            </tr>
                        </table>
                        </td>
                    </tr>

                    <!-- END MAIN CONTENT AREA -->
                    </table>
                    <!-- END CENTERED WHITE CONTAINER -->
    
                    <!-- START FOOTER -->
                    <div class="footer" style="clear: both; margin-top: 10px; text-align: center; width: 100%;">
                        <table role="presentation" border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%;" width="100%">"""
        if footer:
             email +=f"""<tr>
                        <td class="content-block" style="font-family: sans-serif; vertical-align: top; padding-bottom: 10px; padding-top: 10px; color: #999999; font-size: 12px; text-align: center;" valign="top" align="center">
                            <span class="apple-link" style="color: #999999; font-size: 12px; text-align: center;">{footer}</span> 
                        </td>
                        </tr>"""
        email += f"""<tr>
                        <td class="content-block powered-by" style="font-family: sans-serif; vertical-align: top; padding-bottom: 10px; padding-top: 10px; color: #999999; font-size: 12px; text-align: center;" valign="top" align="center">
                            Powered by <a href="http://htmlemail.io" style="color: #999999; font-size: 12px; text-align: center; text-decoration: none;">HTMLemail</a>.
                        </td>
                        </tr>
                    </table>
                    </div>
                    <!-- END FOOTER -->

                </div>
                </td>
                <td style="font-family: sans-serif; font-size: 14px; vertical-align: top;" valign="top">&nbsp;</td>
            </tr>
            </table>
        </body>
        </html>
        """
    return email