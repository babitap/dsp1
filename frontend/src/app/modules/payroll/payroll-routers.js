import Payroll from './views/payroll'

const payrollRoutes = [
    {
        path: 'payroll',
        name: 'payroll',
        component: Payroll,
        meta: {
        breadcrumb: [
            { name: 'Directive Priniciples' }
        ]
        }
    }
]

export default payrollRoutes
