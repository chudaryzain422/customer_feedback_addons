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
        # Create a new customer
        partner = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)
        if not partner:
            partner = request.env['res.partner'].sudo().create({
                'name': name,
                'phone': phone,
                'email': email,
            })
        request.session['feedback_order_id'] = order_id
        request.session['feedback_email'] = email

        survey_url = '/survey/start/feedback_survey'
        return request.redirect(survey_url)








        
    # @http.route('/pos/feedback/submit', type='http', auth='public', website=True, methods=['POST'])
    # def submit_feedback(self, **post):
    #     feedback_id = int(post.get('feedback_id'))
    #     name = post.get('name')
    #     email = post.get('email')
    #     phone = post.get('phone')
    #
    #     # Create or update customer
    #     customer = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)
    #     if not customer:
    #         customer = request.env['res.partner'].sudo().create({
    #             'name': name,
    #             'email': email,
    #             'phone': phone,
    #         })
    #
    #     # Create survey response
    #     feedback = request.env['pos.feedback'].sudo().browse(feedback_id)
    #     if feedback and feedback.survey_id:
    #         # Start survey for the customer
    #         survey_token = feedback.survey_id.sudo()._create_answer(partner=customer)
    #
    #     # Generate discount voucher
    #
    #     coupon = request.env['loyalty.card'].sudo().create({
    #         'program_id': request.env.ref('loyalty_program.discount_program').id,     #here need to add programe created from frontend
    #         'partner_id': customer.id,
    #         'points': 10,  # Assuming 10 points equals a 10% discount
    #     })
    #
    #     expiry_date = datetime.now() + timedelta(days=30)
    #     voucher = request.env['discount.voucher'].sudo().create({
    #         'customer_id': customer.id,
    #         'pos_feedback_id': feedback_id,
    #         'expiry_date': expiry_date,
    #         'state': 'valid',
    #     })
    #
    #     return request.render('pos_feedback.thank_you_page', {
    #         'voucher': coupon
    #     })