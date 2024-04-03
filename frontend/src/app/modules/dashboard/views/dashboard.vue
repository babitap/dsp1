<template>
  <div class="dashboard">


    <EducationDashboard v-if="selectedEntity && selectedEntity.industry_name && (selectedEntity.industry_name.toLowerCase() === 'education' || selectedEntity.industry_name.toLowerCase() === 'demo')" />
    
    <!-- As Behrang Requested: The following is the list of specific clients have customed homepages -->
    <img v-else-if="selectedEntity && selectedEntity.industry_name && selectedEntity.entity_name.toLowerCase() === 'key research'" src="@/assets/img/NZ_Farms_Minified_Text_3_logo.jpg" width="100%" />

    <img v-else-if="selectedEntity && selectedEntity.industry_name && selectedEntity.entity_name.toLowerCase() === 'altra motion'" src="@/assets/img/Altra_Motion_homepage.jpg" width="100%" />

    <img v-else-if="selectedEntity && selectedEntity.industry_name && selectedEntity.entity_name.toLowerCase() === 'operation flinders foundation'" src="@/assets/img/OP_Flinders_Homepage.jpg" width="100%" />

    <img v-else-if="selectedEntity && selectedEntity.industry_name && selectedEntity.entity_name.toLowerCase() === 'yaandina community services'" src="@/assets/img/Yaandina_Homepage.jpg" width="100%" />

    <img v-else-if="selectedEntity && selectedEntity.industry_name && selectedEntity.entity_name.toLowerCase() === 'specialised assistance school for youth (sasy)'" src="@/assets/img/SASY_Homepage.jpg" width="100%" />

    <img v-else-if="selectedEntity && selectedEntity.industry_name && selectedEntity.entity_name.toLowerCase() === 'ilim college'" src="@/assets/img/IlimCollege_Homepage.jpg" width="100%" />

    <img v-else-if="selectedEntity && selectedEntity.industry_name && selectedEntity.entity_name.toLowerCase() === 'pqsa'" src="@/assets/img/PQSA_Homepage.jpg" width="100%" />

    <img v-else-if="selectedEntity && selectedEntity.industry_name && selectedEntity.entity_name.toLowerCase() === 'border express'" src="@/assets/img/BEX_Homepage.jpg" width="100%" />

    <!-- End the list of specific clients have customed homepages -->
  </div>

  
  

</template>

<script>
import { mapState, mapActions } from "vuex";
import EducationDashboard from "../components/education-dashboard"

export default {
  name: "dashboard",
  components: {
        EducationDashboard
    },
  data() {
    return {
    };
  },

  computed: {
    ...mapState({
      selectedEntity: state => state.user.selectedEntity
    })
  },
  methods: {
  },
  watch: {  
  }
};
</script>
