odoo.define('custom_maintenance.my_js', function (require) {"use strict";
    var rpc = require('web.rpc');

    if (location.toString().includes('model=board.board') && location.toString().includes('&view_type=form')) {
        run()
    }
    
    async function run() {
        rpc.query({
            model: 'maintenance.equipment',
            method: 'get_setting',
        }).then(function(data){
            refresh_page_in(data.refresh_time_seconds)
        });
    }

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async function refresh_page_in(refresh_time_seconds) {
        if (refresh_time_seconds > 0) {
            await sleep(refresh_time_seconds*1000);
            location.reload();
        }
    }
});
