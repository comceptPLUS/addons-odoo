# -*- coding: utf-8 -*-
import logging
import datetime
import pytz

from odoo import models, fields, api, modules, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

_logger = logging.getLogger(__name__)


class MailNotification(models.Model):
    _inherit = 'mail.notification'

    message_date_read = fields.Datetime('Date read')


class Message(models.Model):
    _inherit = 'mail.message'

    @api.multi
    def read(self, fields=None, load='_classic_read'):
        res = super(Message, self).read(fields=fields, load=load)

        # Save the date in which the message is read
        for s in self:
            for n in s.notification_ids:
                try:
                    user = self.env['res.users'].search(
                                                        [('partner_id','=',n.res_partner_id.id)],
                                                        limit=1
                                                        )
                    if user.id == self._uid:
                        if not n.message_date_read:
                            n.sudo().write({'message_date_read': datetime.datetime.now()})
                except Exception as e:
                    _logger.error(e)
        return res


    @api.depends('notification_ids.message_date_read')
    @api.multi
    def _get_read_by(self):
        user_tz = self.env.user.tz or 'utc'
        local = pytz.timezone(user_tz)

        for s in self:
            aux = []
            for n in s.notification_ids:
                if n.message_date_read:
                    # This is necessary in order to use the user's timezone
                    # when showing the date (because it's shown in a template)
                    display_date_result = pytz.utc.localize(datetime.datetime.strptime(
                                                                                    n.message_date_read,
                                                                                    DEFAULT_SERVER_DATETIME_FORMAT
                                                                                    )).astimezone(local)
                    if self.env.user.lang:
                        lang = self.env['res.lang'].search([('code','=',self.env.user.lang)])
                        date_format = lang.date_format + ' ' + lang.time_format
                        display_date_result = display_date_result.strftime(date_format)

                    aux_text = "%s (%s)" % (n.res_partner_id.name, display_date_result)
                    aux.append(aux_text)
            s.read_by = ', '.join(aux)

    read_by = fields.Char('Read by', compute='_get_read_by')


    @api.multi
    def message_format(self):
        message_values = self.read([
            'id', 'body', 'date', 'author_id', 'email_from',  # base message fields
            'message_type', 'subtype_id', 'subject',  # message specific
            'model', 'res_id', 'record_name',  # document related
            'channel_ids', 'partner_ids',  # recipients
            'starred_partner_ids',  # list of partner ids for whom the message is starred
            'read_by', #people who read the message
        ])
        message_tree = dict((m.id, m) for m in self.sudo())
        self._message_read_dict_postprocess(message_values, message_tree)

        # add subtype data (is_note flag, subtype_description). Do it as sudo
        # because portal / public may have to look for internal subtypes
        subtype_ids = [msg['subtype_id'][0] for msg in message_values if msg['subtype_id']]
        subtypes = self.env['mail.message.subtype'].sudo().browse(subtype_ids).read(['internal', 'description'])
        subtypes_dict = dict((subtype['id'], subtype) for subtype in subtypes)

        # fetch notification status
        notif_dict = {}
        notifs = self.env['mail.notification'].sudo().search([('mail_message_id', 'in', list(mid for mid in message_tree)), ('is_read', '=', False)])
        for notif in notifs:
            mid = notif.mail_message_id.id
            if not notif_dict.get(mid):
                notif_dict[mid] = {'partner_id': list()}
            notif_dict[mid]['partner_id'].append(notif.res_partner_id.id)

        for message in message_values:
            message['needaction_partner_ids'] = notif_dict.get(message['id'], dict()).get('partner_id', [])
            message['is_note'] = message['subtype_id'] and subtypes_dict[message['subtype_id'][0]]['internal']
            message['subtype_description'] = message['subtype_id'] and subtypes_dict[message['subtype_id'][0]]['description']
            if message['model'] and self.env[message['model']]._original_module:
                message['module_icon'] = modules.module.get_module_icon(self.env[message['model']]._original_module)

            message['read_by'] = message['read_by'] or ''

        return message_values
