from openerp import http
from openerp.http import request

import simplejson
import xlwt
import StringIO

class export_evaluation_report_controller(http.Controller):
    @http.route(['/report/kinesis_athletics_export_evaluation'], type='http', auth='user', website=True, multilang=True)
    def report_account_tax_xls(self, **data):
        data = simplejson.loads(data['options'])

        partner_information = data['partner_information']
        tests = data['tests']
        template_id = data.get('template_id',False)
        if template_id:
            sheet_name = str(template_id) 
        else:
            sheet_name = "sheet" 
        # group_name = data['group_name']

        content = ""

        if tests and partner_information:
            xls = StringIO.StringIO()
            xls_workbook = xlwt.Workbook()
            group_sheet = xls_workbook.add_sheet(sheet_name)

            for r in range(0, len(partner_information)):
                group_sheet.write(r + 1, 0, partner_information[r]['id'])
                group_sheet.write(r + 1, 1, partner_information[r]['name'])

            group_sheet.write(0, 0, 'partner_id')
            group_sheet.write(0, 1, 'Name')
            for r in range(0, len(tests)):
                group_sheet.write(0, r + 2, tests[r])

            xls_workbook.save(xls)
            xls.seek(0)
            content = xls.read()

        return request.make_response(content, headers=[
            ('Content-Type', 'application/vnd.ms-excel'),
            ('Content-Disposition', 'attachment; filename=evaluation.xls;')
        ])