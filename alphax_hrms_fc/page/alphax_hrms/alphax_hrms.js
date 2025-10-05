
frappe.provide('ALX');

frappe.pages['alphax-hrms'].on_page_load = function(wrapper) {
  const page = frappe.ui.make_app_page({ parent: wrapper, title: 'AlphaX HRMS', single_column: true });
  $(frappe.render_template('alphax_hrms', {})).appendTo(page.body);

  loadEmployees();
  loadLeaves();
};

function loadEmployees(){
  const $tb = $('#alx-employees tbody').empty();
  frappe.call({ method:'frappe.client.get_list', args:{ doctype:'Employee', fields:['name','employee_name','company','status','user_id'], limit_page_length:50 }})
    .then(r => (r.message||[]).forEach(e => $tb.append(`<tr><td>${frappe.utils.escape_html(e.name)}</td><td>${frappe.utils.escape_html(e.employee_name||'-')}</td><td>${frappe.utils.escape_html(e.company||'-')}</td><td>${frappe.utils.escape_html(e.status||'-')}</td><td>${frappe.utils.escape_html(e.user_id||'-')}</td></tr>`)));
}

function loadLeaves(){
  const $tb = $('#alx-leaves tbody').empty();
  frappe.call({ method:'frappe.client.get_list', args:{ doctype:'Leave Application', fields:['name','employee_name','leave_type','from_date','to_date','status'], order_by:'creation desc', limit_page_length:50 }})
    .then(r => (r.message||[]).forEach(x => $tb.append(`<tr><td>${frappe.utils.escape_html(x.name)}</td><td>${frappe.utils.escape_html(x.employee_name||'-')}</td><td>${frappe.utils.escape_html(x.leave_type||'-')}</td><td>${frappe.utils.escape_html(x.from_date||'-')}</td><td>${frappe.utils.escape_html(x.to_date||'-')}</td><td>${frappe.utils.escape_html(x.status||'-')}</td></tr>`)));
}

// Leave Application
ALX.leave = {
  openDialog(){
    const d = new frappe.ui.Dialog({
      title: 'Apply Leave',
      fields:[
        {fieldname:'employee', label:'Employee', fieldtype:'Link', options:'Employee', reqd:1},
        {fieldname:'leave_type', label:'Leave Type', fieldtype:'Link', options:'Leave Type', reqd:1},
        {fieldname:'from_date', label:'From Date', fieldtype:'Date', reqd:1},
        {fieldname:'to_date', label:'To Date', fieldtype:'Date', reqd:1},
        {fieldname:'description', label:'Reason', fieldtype:'Small Text'}
      ],
      primary_action_label:'Create & Submit',
      primary_action: (v) => {
        frappe.call({ method:'alphax_hrms_fc.api.leave.create_leave_application', args:v })
          .then(r => frappe.call({ method:'alphax_hrms_fc.api.leave.submit_leave_application', args:{name:r.message.name} }))
          .then(() => { frappe.show_alert({message:'Leave submitted', indicator:'green'}); d.hide(); loadLeaves(); })
          .catch(e => frappe.msgprint({title:'Error', message:e.message || e}));
      }
    });
    d.show();
  }
};

// Attendance with QR/select/scopes
ALX.attendance = {
  check(type){
    const fields = [
      {fieldname:'employee', label:'Employee', fieldtype:'Link', options:'Employee', reqd:1},
      {fieldname:'shift_type', label:'Shift Type', fieldtype:'Link', options:'Shift Type'},
      {fieldname:'branch', label:'Branch', fieldtype:'Link', options:'Branch'},
      {fieldname:'warehouse', label:'Warehouse', fieldtype:'Link', options:'Warehouse'},
      {fieldname:'location', label:'Location', fieldtype:'Link', options:'Location'},
      {fieldname:'project', label:'Project', fieldtype:'Link', options:'Project'},
      {fieldname:'policy', label:'Policy (Auto or Select)', fieldtype:'Select', options:'Auto', default:'Auto'},
      {fieldname:'qr_token', label:'QR Token (if required)', fieldtype:'Password'}
    ];

    const d = new frappe.ui.Dialog({ title:'Attendance Check', fields, primary_action_label:`Check ${type}`, primary_action: doPrimary });

    d.fields_dict.employee.$input.on('change', () => loadPolicies());
    function loadPolicies(){
      const emp = d.get_value('employee'); if(!emp) return;
      frappe.call({ method:'alphax_hrms_fc.api.common.get_policies_for_today', args:{ employee: emp }})
        .then(r => {
          const sel = d.get_field('policy');
          const opts = ['Auto'].concat((r.message||[]).map(p => p.name));
          sel.df.options = opts.join('\n'); sel.refresh();
        });
    }

    // Settings: QR button + geolocation
    frappe.call({ method:'frappe.client.get_value', args:{ doctype:'AlphaX HRMS Settings', fieldname:['enable_qr_scanner_desk','require_geolocation'] }})
      .then(s => {
        const enableQR = s.message && s.message.enable_qr_scanner_desk;
        const requireGeo = s.message && s.message.require_geolocation;
        if (enableQR) {
          d.set_secondary_action_label('Scan QR');
          d.set_secondary_action(() => { ALX.openQrScanner((decoded) => { d.set_value('qr_token', decoded); }); });
        }
        d.__requireGeo = !!requireGeo;
      });

    function doPrimary(){
      const v = d.get_values();
      const args = {
        employee: v.employee,
        log_type: type,
        shift_type: v.shift_type,
        branch: v.branch, warehouse: v.warehouse, location: v.location, project: v.project,
        policy: v.policy && v.policy !== 'Auto' ? v.policy : undefined,
        qr_token: v.qr_token || undefined
      };
      const send = (coords) => {
        if(coords){ args.latitude = coords.latitude; args.longitude = coords.longitude; }
        frappe.call({ method:'alphax_hrms_fc.api.attendance.checkin', args })
          .then(r => { frappe.show_alert({message:`Checked ${type}${r.message.policy? ' @ '+r.message.policy : ''}`, indicator:'green'}); d.hide(); })
          .catch(e => frappe.msgprint({title:'Error', message:e.message||e}));
      };
      if (d.__requireGeo && navigator.geolocation){
        navigator.geolocation.getCurrentPosition(p => send(p.coords), () => frappe.msgprint('Geolocation required.'), {enableHighAccuracy:true, timeout:6000});
      } else if (navigator.geolocation){
        navigator.geolocation.getCurrentPosition(p => send(p.coords), () => send(null), {enableHighAccuracy:true, timeout:4000});
      } else {
        if (d.__requireGeo) return frappe.msgprint('Geolocation required.');
        send(null);
      }
    }

    d.show();
  }
};

// Payslip PDF
ALX.payslip = {
  download(){
    const name = ($('#alx-slip').val()||'').trim();
    if(!name) return frappe.msgprint('Enter Salary Slip ID');
    frappe.call({ method:'alphax_hrms_fc.api.payslip.download_payslip_pdf', args:{ salary_slip: name }})
      .then(r => { const url = r.message && r.message.file_url; if(url) window.open(url, '_blank'); });
  },
  listMine(){
    frappe.call({ method:'alphax_hrms_fc.api.payslip.get_my_payslips', args:{limit:50} })
      .then(r => {
        const rows = r.message || [];
        let html = '<div class="alx-card"><div class="alx-heading">My Payslips</div><div class="table-responsive mt-2"><table class="table table-sm table-alx"><thead><tr><th>ID</th><th>From</th><th>To</th><th>Status</th><th>Gross</th><th>Net</th><th></th></tr></thead><tbody>';
        rows.forEach(x => { html += `<tr><td>${frappe.utils.escape_html(x.name)}</td><td>${x.start_date||'-'}</td><td>${x.end_date||'-'}</td><td>${x.status||'-'}</td><td>${x.gross_pay||'-'}</td><td>${x.net_pay||'-'}</td><td><button class="btn btn-xs btn-primary" onclick="ALX.payslip.dl('${x.name}')">PDF</button></td></tr>`; });
        html += '</tbody></table></div></div>';
        frappe.msgprint({title:'My Payslips', message: html, wide: true});
      });
  },
  dl(name){
    frappe.call({ method:'alphax_hrms_fc.api.payslip.download_payslip_pdf', args:{salary_slip:name} }).then(r => { const url = r.message && r.message.file_url; if(url) window.open(url, '_blank'); });
  }
};
