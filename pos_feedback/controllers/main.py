from odoo import http
from odoo.http import request
from datetime import datetime, timedelta
from odoo.addons.survey.controllers.main import Survey

class SurveyController(Survey):

    @http.route('/survey/submit/<string:survey_token>/<string:answer_token>', type='json', auth='public', website=True)
    def survey_submit(self, survey_token, answer_token, **post):
        response, error = super(SurveyController, self).survey_submit(survey_token, answer_token, **post)
        order_id = request.session.get('feedback_order_id')
        email = request.session.get('feedback_email')
        if order_id and email:
            partner = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)
            if not partner:
                return response, error
            pos_order = request.env['pos.order'].sudo().browse(order_id)
            if pos_order:
                print("hello")
            coupon = request.env['loyalty.card'].sudo().create({
                'program_id': request.env.ref('pos_feedback.10_percent_on_feedback').id,
                'partner_id': partner.id,
                'points': 10,  # Assuming 10 points equals a 10% discount
                'expiration_date': (datetime.today() + timedelta(days=5)).strftime('%Y-%m-%d'),
            })
            request.session.pop('feedback_order_id', None)
            request.session.pop('feedback_email', None)
            print(f"Created loyalty coupon for partner {partner.name}: {coupon.id}")
        return response, error

class POSFeedbackController(http.Controller):

    @http.route('/feedback/form/<int:order_id>', type='http', auth='public', website=True)
    def feedback_form(self, order_id, **kwargs):
        return request.render('pos_feedback.feedback_form_template', {'order_id': order_id})

    @http.route('/feedback/submit', type='http', auth='public', methods=['POST'], website=True)
    def feedback_submit(self, **post):
        order_id = int(post.get('order_id'))
        name = post.get('name')
        phone = post.get('phone')
        email = post.get('email')
        dob = post.get('dob')
        # Create a new customer
        partner = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)
        if not partner:
            partner = request.env['res.partner'].sudo().create({
                'name': name,
                'phone': phone,
                'email': email,
                'date_of_birth': dob,
            })
        request.session['feedback_order_id'] = order_id
        request.session['feedback_email'] = email

        survey = request.env['survey.survey'].sudo().search([('is_feedback_survey', '=', True)], limit=1)
        if not survey:
            survey_url = '/survey/start/feedback_survey'
            return request.redirect(survey_url)
        survey_url = f'/survey/start/{survey.access_token}'
        return request.redirect(survey_url)


