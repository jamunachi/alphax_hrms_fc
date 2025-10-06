
window.ALX = window.ALX || {};

ALX.loadQrLib = function() {
  if (window.Html5Qrcode || window.Html5QrcodeScanner) return Promise.resolve();
  return new Promise((resolve, reject) => {
    frappe.call({ method: "frappe.client.get_value", args: { doctype: "AlphaX HRMS Settings", fieldname: ["qr_lib_url"] }})
      .then(r => {
        const url = (r.message && r.message.qr_lib_url) || "/assets/alphax_hrms_fc/js/vendor/html5-qrcode.min.js";
        const s = document.createElement('script');
        s.src = url;
        s.onload = () => resolve();
        s.onerror = () => reject(new Error("Failed to load QR library"));
        document.head.appendChild(s);
      })
      .catch(() => reject(new Error("Failed to read settings")));
  });
};

ALX.openQrScanner = function(onSuccess) {
  const wrap = new frappe.ui.Dialog({ title: 'Scan QR', size: 'large' });
  const id = 'alx-qr-area-' + (Date.now());
  wrap.$body.html(`<div id="${id}"></div>`);
  const start = () => {
    if (!window.Html5QrcodeScanner) { frappe.msgprint('QR library missing.'); return; }
    const scanner = new Html5QrcodeScanner(id, { fps: 10, qrbox: 250 });
    scanner.render((decoded) => {
      try { onSuccess && onSuccess(decoded || ''); } finally { scanner.clear().then(()=>wrap.hide()); }
    }, (err) => {/* ignore scan errors */});
  };
  ALX.loadQrLib().then(start).catch(e => frappe.msgprint(e.message || e));
  wrap.show();
};
