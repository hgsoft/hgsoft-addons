# -*- coding: utf-8 -*-

from email.utils import parseaddr, formataddr

from odoo import models, fields, api


class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    user_id = fields.Many2one('res.users', string="Owner")
    email_name = fields.Char('Email Name', help="Overrides default email name")
    force_use = fields.Boolean(
        'Force Use',
        help="If checked and this server is chosen to send mail message, "
        "It will ignore owners mail server")

    @api.model
    def replace_email_name(self, old_email):
        """
        Replaces email name if new one is provided
        """
        if self.email_name:
            old_name, email = parseaddr(old_email)
            return formataddr((self.email_name, email))
        else:
            return old_email


class MailMail(models.Model):
    _inherit = 'mail.mail'

    @api.multi
    def send(self, auto_commit=False, raise_exception=False):
        """Extend to send using Mail server by user.

        Will use such mail server only if there is one with user
        specified.
        """
        IrMailServer = self.env['ir.mail_server']
        for mail in self:
            if not mail.mail_server_id.force_use:
                user_ids = mail.author_id.user_ids
                if user_ids:
                    user_id = user_ids[0].id
                    mail_server = IrMailServer.search(
                        [('user_id', '=', user_id)], limit=1)
                    if mail_server:
                        mail.mail_server_id = mail_server.id
            mail.email_from = mail.mail_server_id.replace_email_name(
                mail.email_from)
        return super(MailMail, self).send(auto_commit=auto_commit,
                                          raise_exception=raise_exception)
