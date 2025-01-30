/** @odoo-module */

import { Order } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";
import { qrCodeSrc } from "@point_of_sale/utils";

patch(Order.prototype, {
    //@override
    export_for_printing() {
        debugger;
        return {
            ...super.export_for_printing(...arguments),
            feedback_qr_code: qrCodeSrc(`${this.pos.base_url}/feedback/form/${this.server_id}`),
        };
    },
});
