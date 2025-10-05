
(() => {
  frappe.ready(() => {
    frappe.call({ method: "alphax_hrms_fc.api.theme.get_active_theme" }).then(r => {
      const d = (r && r.message) || {};
      const map = {
        "--primary": d.button_background_color,
        "--secondary": d.button_hover_background_color,
        "--text-on-primary": d.button_text_color,
        "--heading-color": d.heading_text_color,
        "--muted-bg": d.box_background_color,
      };
      Object.entries(map).forEach(([k,v]) => v && document.documentElement.style.setProperty(k, v));
    });
  });
})();
