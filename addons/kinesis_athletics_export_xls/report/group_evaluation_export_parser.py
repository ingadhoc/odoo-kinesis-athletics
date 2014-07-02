# import time
# from openerp.tools.translate import _

# from openerp.report import report_sxw
# from openerp.report.report_sxw import rml_parse
import time
from openerp.report import report_sxw


class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        
        # El tema es que esto ni siquiera me lo toma el aeroo, no lee el parser
        self.lang = context.get('lang', 'es_ES')
        tests = self.pool['kinesis_athletics.test'].browse(cr, uid, context['tests'], context=context)
        # Fijate que este print ni siquiera se imprime
        print 'TESTS', tests        
        company_id = self.pool.get('res.users').browse(cr, uid, [uid])[0].company_id         
        
        self.localcontext.update({
            'lang': self.lang,
            'tests': self.tests,
            'company_logo': company_id.logo,
            'today': time.localtime(),
        })
