<template>
  <aside
    class="app-sidebar"
    :class="computedClass"
    :style="computedStyle"
  >
    <ul class="app-sidebar__menu">
      <template v-for="(item, key) in items">
        <app-sidebar-link-group
          :key="key"
          :minimized="minimized"
          :icon="item.meta && item.meta.iconClass"
          v-if="item.children"
          :title="item.displayName"
          :children="item.children"
          :active-by-default="hasActiveByDefault(item)"
        >
          <app-sidebar-link
            v-for="(subMenuItem, key) in item.children"
            :key="key"
            :to="{ name: subMenuItem.name , params: subMenuItem.params }"
            :title="subMenuItem.displayName"
          />
        </app-sidebar-link-group>
        <app-sidebar-link
          v-else
          :key="key"
          :minimized="minimized"
          :active-by-default="item.name === $route.name"
          :icon="item.meta && item.meta.iconClass"
          :to="{ name: item.name }"
          :title="item.displayName"
        />
      </template>
    </ul>
  </aside>
</template>

<script>
import { educationMenuItems, defaultMenuItems , payrollMenuItems} from '@/app/shared/menu-items'
import AppSidebarLink from './components/app-sidebar-link'
import AppSidebarLinkGroup from './components/app-sidebar-link-group'
import { ColorThemeMixin } from '@/services/vuestic-ui'
import { mapState, mapActions } from "vuex";
//import VaIconMenu from '@/iconset/VaIconMenu'

export default {
  name: 'app-sidebar',
  inject: ['contextConfig'],
  components: {
    AppSidebarLink,
    AppSidebarLinkGroup,
  },
  mixins: [ColorThemeMixin],
  props: {
    minimized: {
      type: Boolean,
      required: true,
    },
    color: {
      type: String,
      default: 'secondary',
    },
  },
  data () {
    return {
      //items: defaultMenuItems.routes,
      default_items : [],
      reports_items : [],
      download_items : [],
      export_items : []
    }
  },
  

  computed: {
      ...mapState({
      selectedEntity: state => state.user.selectedEntity,
      entityLookUpList: state => state.user.entityLookUpList,
      availableReports: state => state.report.availableReports,
      availableDownloads: state => state.download.availableDownloads,
      availableExports: state => state.powerbiExport.availableExports,
    }),
    computedClass () {
      return {
        'app-sidebar--minimized': this.minimized,
      }
    },
    computedStyle () {
      return {
        backgroundColor: this.contextConfig.invertedColor ? this.$themes.dark2 : this.colorComputed,
      }
    },
    items(){
      return [ ...this.default_items, ...this.reports_items, ...this.download_items, ...this.export_items ]
    }
  },
  async created(){
      if( this.selectedEntity.id ){
        this.getReportList(newValue.id)
        this.getDownloadList(newValue.id)
        this.getExportList(newValue.id)
        this.default_items = this.getDefaultMenu(this.selectedEntity.industry_name)
      }
  },

  watch: {
      selectedEntity(newValue){
          if(newValue) {

            this.default_items = this.getDefaultMenu(this.selectedEntity.industry_name);

            this.reports_items = []; 
            this.getReportList(newValue.id); 

            this.download_items = []; 
            this.getDownloadList(newValue.id)

            this.export_items = []; 
            this.getExportList(newValue.id)

          
          }
      },
      availableReports(newValue){

        const categories = Object.keys(newValue);
        let reports = []
        categories.forEach(c => {
            let cate = {name: 'report', displayName: `${c} `, meta: {iconClass: 'entypo entypo-folder'}}
            cate.children = []
            newValue[c].forEach(r => {
                let report = {name: 'report', displayName: `${r.name}`, params: {codename: `${r.codename}`}, meta: {iconClass: 'vuestic-iconset vuestic-iconset-files'}}
                cate.children.push(report)
            })
            reports.push(cate)
        })
        this.reports_items = reports; 
      },
      availableDownloads(newValue){
        let downloads = []
        if( newValue.length > 0 ){
          let download_cate = {name: 'download', displayName: `Download `, meta: {iconClass: 'entypo entypo-download'}}
          download_cate.children = []
          for( var i = 0; i<newValue.length; i++ ){
            var id = newValue[i].id; 
            var name = newValue[i].name; 
            let report = {name: 'download', displayName: `${name}`, params: {download_id: `${id}`, download_name:`${name}`}, meta: {iconClass: 'vuestic-iconset vuestic-iconset-files'}}
            download_cate.children.push(report); 
          }
          downloads.push(download_cate); 
        }
      
        this.download_items = downloads; 
      },
      availableExports(newValue){
        let exports = []
        if( newValue.length > 0 ){
          let export_cate = {name: 'export', displayName: `Export `, meta: {iconClass: 'entypo entypo-export'}}
          export_cate.children = []
          for( var i = 0; i<newValue.length; i++ ){
            var id = newValue[i].id; 
            var name = newValue[i].name; 
            let report = {name: 'export', displayName: `${name}`, params: {export_id: `${id}`, export_name:`${name}`}, meta: {iconClass: 'vuestic-iconset vuestic-iconset-files'}}
            export_cate.children.push(report); 
          }
          exports.push(export_cate); 
        }

        this.export_items = exports; 
      },



      
  },
  methods: {
      ...mapActions({
            getReportList: "report/getReportList",
            getDownloadList: "download/getDownloadList",
            getExportList: "powerbiExport/getExportList",
        }),
    hasActiveByDefault (item) {
      return item.children.some(child => child.name === this.$route.name)
    },

    getDefaultMenu(industryName){
        let menu = defaultMenuItems.routes
        
        if(industryName){
          console.log('industryname is:',industryName)
            switch (industryName.toLowerCase()) {
                case 'education':
                {
                  menu = [...menu, ...educationMenuItems.routes];
                  break;
                }
                case 'demo':
                {
                  menu = [...menu, ...educationMenuItems.routes];
                  break;
                }
                case 'payroll':
                {
                  menu = [];
                  menu = [...menu, ...payrollMenuItems.routes];
                  break;
                }
            }
        }
        console.log("_debug: ", this.selectedEntity.entity_name.toLowerCase())
        // Change "Dashboard" name to "Home" for the following clients 
        // <!-- As Behrang Requested: The following is the list of specific clients have customed homepages -->
        if ( ["key research", "altra motion", "operation flinders foundation", "yaandina community services", "specialised assistance school for youth (sasy)", "ilim college", "pqsa"].includes(this.selectedEntity.entity_name.toLowerCase())) {
          var i;
          for (i = 0; i < menu.length; i++) {
            if (menu[i].name === "dashboard" && menu[i].displayName === "Dashboard") {
              menu[i].displayName = "Home";
              break;
            }
          };
        } else {
          var i;
          for (i = 0; i < menu.length; i++) {
            if (menu[i].name === "dashboard" && menu[i].displayName === "Home") {
              menu[i].displayName = "Dashboard";
              break;
            }
          };
        }

        return menu
    }
     
  }
}

</script>

<style lang="scss">
.app-sidebar {
  overflow: auto;
  display: flex;
  max-height: 100%;
  flex: 0 0 16rem;

  @include media-breakpoint-down(sm) {
    flex: 0 0 100%;
  }

  &--minimized {
    flex: 0 0 3.25rem;
  }

  &__menu {
    margin-bottom: 0;
    padding-top: 2.5625rem;
    padding-bottom: 2.5rem;
    list-style: none;
    padding-left: 0;
    width: 100%;
  }
}
</style>
