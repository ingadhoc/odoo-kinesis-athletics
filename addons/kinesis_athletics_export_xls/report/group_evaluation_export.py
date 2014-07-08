from openerp import http
from openerp.http import request
from openerp.osv import osv

import simplejson
import xlwt
import StringIO


class group_evaluation_export_xls(http.Controller):
    @http.route(['/report/kinesis_athletics_group_evaluation_export_xls'], type='http', auth='user', website=True, multilang=True)
    def report_account_tax_xls(self, **data):
        #data = simplejson.loads(data['options'])

#        vat = tax_report(request.cr, request.uid, '', context=request.context)
#        vat.set_context(None, data, None)
#        lines = vat._get_lines(vat._get_basedon(data), company_id=data['form']['company_id'])

#        if lines:
#            xls = StringIO.StringIO()
#            xls_workbook = xlwt.Workbook()
#            vat_sheet = xls_workbook.add_sheet('report_vat')
#            for x in range(0, len(lines)):
#                for y in range(0, len(lines[0])):
#                    vat_sheet.write(x, y, lines[x].values()[y])
#            xls_workbook.save(xls)
#            xls.seek(0)
#            content = xls.read()
        content = ""
        return request.make_response(content, headers=[
            ('Content-Type', 'application/vnd.ms-excel'),
            ('Content-Disposition', 'attachment; filename=evaluation.xls;')
        ])