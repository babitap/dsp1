import Download from './views/download'

const downloadRoutes = [
    {
        path: 'download/:download_id',
        name: 'download',
        component: Download,
        props: true,
        meta: {
            breadcrumb: [
                { name: 'Download' }
          ],
            requiresDownloadPermission: true
        }
    },
    {
        path: 'download',
        redirect: { name: 'dashboard' },
        name: 'download',
        component: Download,
        meta: {
            breadcrumb: [
                { name: 'Report' }
            ]
        }
    }    
]

export default downloadRoutes


