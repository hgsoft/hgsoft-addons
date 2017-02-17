openerp.revert_compose_message = function (session) {
    var _t = session.web._t, _lt = session.web._lt;



    /**
     * ------------------------------------------------------------
     * UserMenu
     * ------------------------------------------------------------
     *
     * Add a link on the top user bar for write a full mail
     */
    session.web.ComposeMessageTopButton = session.web.Widget.extend({
        template:'revert_compose_message.ComposeMessageTopButton',

        start: function () {
            this.$el.on('click', this.on_compose_message);
            this._super();
        },

        on_compose_message: function (event) {
            event.preventDefault();
            event.stopPropagation();
            var action = {
                type: 'ir.actions.act_window',
                res_model: 'mail.compose.message',
                view_mode: 'form',
                view_type: 'form',
                views: [[false, 'form']],
                target: 'new',
                context: {},
            };
            session.client.action_manager.do_action(action);
        },
    });

    session.web.UserMenu.include({
        do_update: function(){
            var self = this;
            this._super.apply(this, arguments);
            this.update_promise.then(function() {
                var mail_button = new session.web.ComposeMessageTopButton();
                mail_button.appendTo(session.webclient.$el.parents().find('.oe_systray'));
                openerp.web.bus.trigger('resize');  // Re-trigger the reflow logic
            });
        },
    });
}