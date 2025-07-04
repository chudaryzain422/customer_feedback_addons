/** @odoo-module */

import { RefundButton } from "@point_of_sale/app/screens/product_screen/control_buttons/refund_button/refund_button";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";

patch(RefundButton.prototype, {
    setup(){
        super.setup();
        this.user = useService("user");
    },
    async click() {
        this.userHasRefundAccess = await this.user.hasGroup("AN_pos_refund_access.group_refund");
        if (!this.userHasRefundAccess) {
            this.showCustomPopup("You do not have permission to process refunds.");
            return;
        }
        return super.click();
    },

    showCustomPopup(message) {
        const popupDiv = document.createElement("div");
        popupDiv.innerHTML = `
            <div id="customPopup" style="
                position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
                background: white; padding: 20px; border-radius: 10px;
                box-shadow: 0px 4px 6px rgba(0,0,0,0.2); text-align: center;
                z-index: 10000;
            ">
                <p style="font-size: 16px; color: red;">${message}</p>
                <button id="popupCloseBtn" style="
                    padding: 5px 15px; background: red; color: white;
                    border: none; border-radius: 5px; cursor: pointer;
                ">Close</button>
            </div>
        `;
        document.body.appendChild(popupDiv);
        document.getElementById("popupCloseBtn").addEventListener("click", () => {
            document.getElementById("customPopup").remove();
        });
    }
});
