<template>
  <div class="selectionContainer">
    <div class="">
      <va-tabs grow v-model="selectedTabIndex">
        <va-tab v-for="title in tabOptions" :key="title">{{title}}</va-tab>
      </va-tabs>
    </div>
    <div class="selectionContent">
      <div v-show="selectedTabIndex === 0"  class="reportManagementContainer">
        <ReportManagement
          @openEditReportModal="openEditReportModal"
          @removeReport="removeReport"/>
      </div>
      <div v-show="selectedTabIndex === 1"  class="entityManagementContainer">
        <EntityManagement/>
      </div>            
      <div v-show="selectedTabIndex === 2"  class="superUserInviteContainer">
        <InviteSpecialUser/>
      </div>


    </div>
  </div>
</template>

<script>
import InviteSpecialUser from "../components/invite-special-user"
import EntityManagement from "../components/entity-management"
import ReportManagement from "../components/report-management"

export default {
  name: "super-user-management",
  components:{
      InviteSpecialUser,
      EntityManagement,
      ReportManagement
  },
  props: {
    openEditReportModal: { type: Function },
    removeReport: { type: Function }
  },
  data() {
    return {
      selectedTabIndex: 0,
      tabOptions: ["Report Management", "Entity Management","Special User Management" ],
    };
  }
}
</script>

<style lang="scss" scoped>
.selectionContainer {
  width: 100%;
  background-color: white;
  border-radius: 0.375rem;
  border: none;

  & .selectionContent > div {
    display: flex;
    justify-content: center;
  }
}
</style>