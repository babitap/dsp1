import PowerBIExport from './views/powerbi-export'

const powerbiExportRoutes = [
    {
        path: 'export/:export_id',
        name: 'export',
        component: PowerBIExport,
        props: true,
        meta: {
            breadcrumb: [
                { name: 'Export' }
          ],
            requiresDownloadPermission: true
        }
    },
    {
        path: 'export',
        redirect: { name: 'dashboard' },
        name: 'export',
        component: PowerBIExport,
        meta: {
            breadcrumb: [
                { name: 'Report' }
            ]
        }
    }
]

export default powerbiExportRoutes


