from odoo import http
from odoo.addons.test_impex.tests.test_load import message
from odoo.http import request
from datetime import datetime, timedelta
from odoo.addons.survey.controllers.main import Survey
import requests
import json
import logging

_logger = logging.getLogger(__name__)


class SurveyController(Survey):

    @http.route('/survey/submit/<string:survey_token>/<string:answer_token>', type='json', auth='public', website=True)
    def survey_submit(self, survey_token, answer_token, **post):
        response, error = super(SurveyController, self).survey_submit(survey_token, answer_token, **post)
        _logger.info("Entered in submit suravy controller")
        order_id = request.session.get('feedback_order_id')
        email = request.session.get('feedback_email')
        partner = request.session.get('feedback_partner')
        if order_id and email:
            partner = request.env['res.partner'].sudo().search([('id', '=', partner)], limit=1)
            if not partner:
                return response, error
            pos_order = request.env['pos.order'].sudo().browse(order_id)
            if pos_order:
                _logger.info("hello")
                print("hello")
            coupon = request.env['loyalty.card'].sudo().create({
                'program_id': request.env.ref('pos_feedback.10_percent_on_feedback').id,
                'partner_id': partner.id,
                'points': 10,  # Assuming 10 points equals a 10% discount
                'expiration_date': (datetime.today() + timedelta(days=5)).strftime('%Y-%m-%d'),
            })
            partner.barcode = coupon.code
            self.send_whatsapp_message(partner, coupon)
            request.session.pop('feedback_order_id', None)
            request.session.pop('feedback_email', None)
            request.session.pop('feedback_partner', None)
            _logger.info(f"Created loyalty coupon for partner {partner.name}: {coupon.code}")
            print(f"Created loyalty coupon for partner {partner.name}: {coupon.id}")
        return response, error



    def send_whatsapp_message(self, partner, coupon):
        # Implement your WhatsApp message-sending logic here.
        try:
            if partner.mobile:
                provider = request.env['provider'].sudo().search([('state', '=', 'enabled'), ('provider', '=', 'graph_api')], limit=1)
                if provider and provider.graph_api_authenticated:
                    template = request.env['wa.template'].sudo().search([('state', '=', 'added'),('provider_id', '=', provider.id),('name', '=', 'ambi')], limit=1)
                    compose = request.env['wa.compose.message'].sudo().with_context(active_model="res.partner", active_id=partner.id).create({
                        'partner_id':partner.id,
                        'provider_id':provider.id,
                        'template_id':template.id,
                        'company_id':provider.company_id.id,
                    })
                    if compose:
                        compose.sudo().onchange_template_id_wrapper()
                        compose.sudo().send_whatsapp_message()
                        _logger.info(f"Sent WhatsApp message to {partner.mobile} and code is {partner.barcode}")
                    print(f"Sent WhatsApp message to {partner.mobile}")
            else:
                _logger.info(f"No phone number available for partner {partner.name}. WhatsApp message not sent.")
                print(f"No phone number available for partner {partner.name}. WhatsApp message not sent.")
        except Exception as e:
            # Catch any error that occurs in the process
            _logger.error(f"Error sending WhatsApp message to {partner.name} ({partner.id}): {str(e)}")
            print(f"Error sending WhatsApp message to {partner.name} ({partner.id}): {str(e)}")

class POSFeedbackController(http.Controller):

    @http.route('/feedback/form/<int:order_id>', type='http', auth='public', website=True)
    def feedback_form(self, order_id, **kwargs):
        return request.render('pos_feedback.feedback_form_template', {'order_id': order_id})

    @http.route('/feedback/submit', type='http', auth='public', methods=['POST'], website=True)
    def feedback_submit(self, **post):
        order_id = int(post.get('order_id'))
        name = post.get('name')
        mobile = post.get('mobile')
        email = post.get('email')
        dob = post.get('dob')
        # Create a new customer
        partner = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)
        if not partner:
            partner = request.env['res.partner'].sudo().create({
                'name': name,
                'mobile': mobile,
                'phone': mobile,
                'email': email,
                'date_of_birth': dob,
            })
        request.session['feedback_order_id'] = order_id
        request.session['feedback_email'] = email
        request.session['feedback_partner'] = partner.id

        survey = request.env['survey.survey'].sudo().search([('is_feedback_survey', '=', True)], limit=1)
        if not survey:
            survey_url = '/survey/start/feedback_survey'
            return request.redirect(survey_url)
        survey_url = f'/survey/start/{survey.access_token}'
        return request.redirect(survey_url)


