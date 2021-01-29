# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from collections import defaultdict

class CustomMailActivity(models.Model):
    _inherit = "mail.activity"
    
    show_user_ids = fields.Boolean(default=True)
    
    user_ids = fields.Many2many('res.users', 'mail_activities_user_ids', 'activity_id', 'user_id', string='Recipients', index=True)
        
    revision_id = fields.Text(string='Revision Id')
    
    revision_name = fields.Text(string='Revision Name')
    
    revision_summary = fields.Text(string='Revision Summary')
    
    revision_write_user_name = fields.Text(string='Revision User Name')
    
    revision_write_date = fields.Datetime(string='Revision Write Date')
    
    revision_state = fields.Selection([ ('in_progress', 'In progress'),('done', 'Done'),],'Revision State', default='in_progress')
    
    document_display_name = fields.Text(string="Document Display Name", compute='_get_document_display_name', store=True)
        
    user_department_id = fields.Many2one(related='user_id.department_id', string="User Department", store=True)
    
    @api.depends('res_name', 'revision_name')
    def _get_document_display_name(self):
        for record in self:
            record.document_display_name = "{} [{}]".format(record.res_name, record.revision_name)

    @api.model
    def create(self, vals):
        model = self.env.context['default_res_model']
        
        if model == 'document.page':
            object_id = self.env.context['default_res_id']
            document_page = self.env[model].search([['id', '=', object_id]])
            vals['revision_id'] = document_page.history_ids[0].id
            vals['revision_name'] = document_page.history_ids[0].name
            vals['revision_summary'] = document_page.history_ids[0].summary
            vals['revision_write_user_name'] = document_page.history_ids[0].write_uid.name
            vals['revision_write_date'] = document_page.history_ids[0].write_date
            
        user_ids = [vals['user_id']] + vals['user_ids'][0][2]
        vals['user_ids'] = None
        vals['show_user_ids'] = False
        rec = None

        for user_id in user_ids:
            vals['user_id'] = user_id
            rec = super(CustomMailActivity, self).create(vals)
            
        return rec
    
    def _action_done(self, feedback=False, attachment_ids=None):        
        """ Private implementation of marking activity as done: posting a message, deleting activity
            (since done), and eventually create the automatical next activity (depending on config).
            :param feedback: optional feedback from user when marking activity as done
            :param attachment_ids: list of ir.attachment ids to attach to the posted mail.message
            :returns (messages, activities) where
                - messages is a recordset of posted mail.message
                - activities is a recordset of mail.activity of forced automically created activities
        """
        # marking as 'done'
        messages = self.env['mail.message']
        next_activities_values = []

        # Search for all attachments linked to the activities we are about to unlink. This way, we
        # can link them to the message posted and prevent their deletion.
        attachments = self.env['ir.attachment'].search_read([
            ('res_model', '=', self._name),
            ('res_id', 'in', self.ids),
        ], ['id', 'res_id'])

        activity_attachments = defaultdict(list)
        for attachment in attachments:
            activity_id = attachment['res_id']
            activity_attachments[activity_id].append(attachment['id'])

        for activity in self:
            # extract value to generate next activities
            if activity.force_next:
                Activity = self.env['mail.activity'].with_context(activity_previous_deadline=activity.date_deadline)  # context key is required in the onchange to set deadline
                vals = Activity.default_get(Activity.fields_get())

                vals.update({
                    'previous_activity_type_id': activity.activity_type_id.id,
                    'res_id': activity.res_id,
                    'res_model': activity.res_model,
                    'res_model_id': self.env['ir.model']._get(activity.res_model).id,
                })
                virtual_activity = Activity.new(vals)
                virtual_activity._onchange_previous_activity_type_id()
                virtual_activity._onchange_activity_type_id()
                next_activities_values.append(virtual_activity._convert_to_write(virtual_activity._cache))

            # post message on activity, before deleting it
            record = self.env[activity.res_model].browse(activity.res_id)
            record.message_post_with_view(
                'mail.message_activity_done',
                values={
                    'activity': activity,
                    'feedback': feedback,
                    'display_assignee': activity.user_id != self.env.user
                },
                subtype_id=self.env['ir.model.data'].xmlid_to_res_id('mail.mt_activities'),
                mail_activity_type_id=activity.activity_type_id.id,
                attachment_ids=[(4, attachment_id) for attachment_id in attachment_ids] if attachment_ids else [],
            )

            # Moving the attachments in the message
            # TODO: Fix void res_id on attachment when you create an activity with an image
            # directly, see route /web_editor/attachment/add
            activity_message = record.message_ids[0]
            message_attachments = self.env['ir.attachment'].browse(activity_attachments[activity.id])
            if message_attachments:
                message_attachments.write({
                    'res_id': activity_message.id,
                    'res_model': activity_message._name,
                })
                activity_message.attachment_ids = message_attachments
            messages |= activity_message

        next_activities = self.env['mail.activity'].create(next_activities_values)

        ### \/ OVERRIDE \/ ###
        if self.revision_id:
            # New rule for change status instead of unlink()
            self.revision_state = 'done'
            
        else:
            self.unlink()  # will unlink activity, dont access `self` after that
        ### /\ OVERRIDE /\ ###

        return messages, next_activities
        
    @api.onchange('user_id')
    def _user_id_onchange(self):
        self.user_ids = None

        if self._ids[0].origin == False:
            # Criação
            return {'domain': {'user_ids': [('user_ids', '!=', self.user_id.id)]}}
        else:
            # Edição
            return {'domain': {'user_ids': [('user_ids', '=', None)]}}
    
    @api.onchange('user_ids')
    def _user_ids_onchange(self):
        if self._ids[0].origin == False:
            # Criação
            return {'domain': {'user_ids': [('user_ids', '!=', self.user_id.id)]}}
        else:
            # Edição
            return {'domain': {'user_ids': [('user_ids', '=', None)]}}

class CustomMailActivityType(models.Model):
    _inherit = 'mail.activity.type'
    
    display_in_master_list = fields.Boolean("Display in Master List ?", default=False)


class CustomHrEmployeeBase(models.AbstractModel):
    _inherit = "hr.employee.base"

    @api.constrains('department_id')
    def _update_activity_department(self):
        mail_activity_obj = self.env['mail.activity'].search([['user_id', '=', self.user_id.id]])
        if mail_activity_obj:
            mail_activity_obj.write({'user_department_id': self.department_id.id})
    
class CustomDocumentPage(models.Model):
    _inherit = "document.page"
    
    @api.depends("history_ids")
    def _compute_history_head(self):
        for rec in self:
            if rec.history_ids:
                rec.history_head = rec.history_ids[0]
            else:
                default_draft_name = _("Review 00")
                default_draft_summary = _("Initial review")
                rec.history_head = False
                rec.draft_name = default_draft_name
                rec.draft_summary = default_draft_summary

