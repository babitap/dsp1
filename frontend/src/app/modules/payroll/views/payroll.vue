<template>
  <div id="main-container">
    <modals-container @savedata="handleSaveRule" @editdata="handleEditRule"/>
    <Header />
    <div class="row" style="justify-content: center;" v-if="this.isFileUploaded == false">
      <div v-if="uploadFile !== null" style="padding-right: 5rem;">
        File Selected  <p>{{ uploadFile.name }}</p>
      </div>
      <FileUploader v-if="uploadFile == null" @change="handleFileChange" />
      <div style="margin-left: 5rem;" v-if="uploadFile !== null">
        <div class="row">
          <ActionButton label="Submit Documents"  @button-clicked="handleButtonClick" />
        </div>
      </div>
    </div>
    <hr>
    <div class="row row-equal">
      <div class="flex xs12">
        <va-card class="va-card-style">
          <div class="row">
            <Header title="Rules" />
            <div class="flex xs12">
              <PayrollTabs :tabNames="tabNames" v-model="selectedDataSetIndex"/>
            </div>
          </div>
          <va-card class="va-card-style-internal">
            <div class="row">
              <div class="flex xs12">
                <p>List of rules ready for review</p>
                <hr>
                <!----<div class="flex xs3">
                  <va-select
                    v-model="employmentType"
                    :options="employmentTypeOptions"
                    noClear
                  />
                </div>-->
                <PayrollDataTable
                  :selectedDataSetIndex="selectedDataSetIndex"
                  :items="getItemsForSelectedTab"
                  :fields="fields"
                  :isCheckedArray="checkedArray"
                  @editRule="openEditRuleModal"
                />
              </div>
            </div>
            <div class="action-buttons">
              <va-button medium @click="openCreateRuleModal()">Add a New Rule</va-button>
              <va-button medium @click="handleFinalButtonClick">Final Review & Sign off</va-button>
            </div>

        <div v-if="isModalVisible" class="modal-overlay">
          <div class="modal">
           <h6 style="font-size: 1.5rem;"> Final Sign Off Confimation</h6>
           <br/>
           <br/>
           <p style="font-size: large;"> Thank you for Reviewing and Sign-Off award document.</p>
           <br/>
           <va-button medium style="float: right;" @click="closeModal">Close</va-button>
          </div>
        </div>

          </va-card>
        </va-card>
      </div>
    </div>
  </div>

</template>

<script>

import PayrollDataTable from "./components/PayrollDataTable.vue";
import CreateRuleModal from "./components/CreateRuleModal.vue";
import EditRuleModal from "./components/EditRuleModal.vue";
import Header from "./components/Header.vue";
import FileUploader from "./components/FileUploader.vue";
import ActionButton from "./components/ActionButton.vue";
import PayrollTabs from "./components/PayrollTabs.vue";
import ActionButtons from "./components/ActionButtons.vue";
import VModal from 'vue-js-modal/dist/ssr.index';
import { httpClient } from '@/app/shared/services/http-client'
import { loadingService } from '@/app/shared/services/loading-service'

export default {
  name: "payroll",
  components: {
    PayrollDataTable,
    Header,
    FileUploader,
    ActionButton,
    PayrollTabs,
    ActionButtons,
    CreateRuleModal,
    EditRuleModal
  },
  data () {
    return {
      itemsShift :  [],
      itemsOvertime :  [],
      itemsRDO :  [],
      itemsAllowance :  [],
      itemsLeave :  [],
      itemsSuper :  [],
      itemsMiscellaneous: [],

      uploadFile: null,
      uploadFileContent: null,

      selectedDataSetIndex: 0,
      isChecked: false,
      isFileUploaded: false,
      isModalVisible : false,
      showDeleteConfirmationDialog: false,
      employmentType: 'Employment Type',
      employmentTypeOptions: ['Permanent', 'Casual/Part Time', 'Contract', 'Full Time'],
      tabNames: [ 'Shift', 'Overtime', 'RDO', 'Allowance', 'Leave', 'Super', 'Miscellaneous'],
    }
  },
  computed: {
    getItemsForSelectedTab() {
      if(this.isFileUploaded)
      {
        
        switch (this.selectedDataSetIndex) {
          case 0:
            return this.itemsShift;
          case 1:
            return this.itemsOvertime;
          case 2:
            return this.itemsRDO;
          case 3:
            return this.itemsAllowance;
          case 4:
            return this.itemsLeave;
          case 5:
            return this.itemsSuper;
          case 6:
            return this.itemsMiscellaneous
          default:
            return this.itemsShift;
         }
      } else {
        return []
      }


    },
    fields () {
      return [
        {
          name: 'number',
          title: 'Iter#',
          sortField: 'number',
          width: '5%',
        },
        {
          name: 'Rule',
          title: 'Description',
          sortField: 'description',
          width: '60%',
        },
        {
          name: 'comment',
          title: 'Comment',
          sortField: 'comment',
          width: '35%',
        },
        {
          name: '__slot:actionssel',
          dataClass: 'text-right',
        },
        {
          name: '__slot:actions',
          dataClass: 'text-right',
        }
      ]
    },

  },

  methods: {
    openCreateRuleModal(){
      this.$modal.show(CreateRuleModal,
                {
                    title: 'Create New Rule',
                    propsCategory: "",
                    propsComment: ""
                },
                {
                    isAutoHeight: true,
                    resizable: false,
                    adaptive: true,
                    draggable: true,
                    root: this.$root
                },
            )
    },
    handleSaveRule(childData) {
      const currentItems = this.getItemsForSelectedTab
      currentItems.push({
        number: currentItems.length + 1,
        Rule: childData.description,
        comment: childData.memo
      })
    },
    handleEditRule(childData) {
      console.log(childData)
      const currentItems = this.getItemsForSelectedTab
      const foundItem = currentItems.find(item => item.number === childData.number)
      console.log(foundItem)
      if (foundItem) {
        foundItem.Rule = childData.description
        foundItem.comment = childData.memo
      }
    },
    openEditRuleModal(itemData) {
      console.log('1', itemData)
      this.$modal.show(EditRuleModal,
                {
                    title: 'Edit Rule',
                    propsCategory: itemData.Rule,
                    propsComment: itemData.comment,
                    propsNumber: itemData.number
                },
                {
                    isAutoHeight: true,
                    resizable: false,
                    adaptive: true,
                    draggable: true,
                    root: this.$root
                },
            )
    },
    openFileInput() {
      this.$refs.fileInput.click();
    },
    handleFileChange(event) {
      const selectedFile = event.target.files[0]
      this.uploadFile = selectedFile
      this.displaySelectedImage(selectedFile)
    },
    displaySelectedImage(file) {
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.selectedImage = e.target.result;
        };
        reader.readAsDataURL(file)
      }
    },

    async handleButtonClick() {
      const self = this
      loadingService.showLoading(true);
      var formData = new FormData();
      console.log(this.uploadFile)
      formData.append('file', this.uploadFile, this.uploadFile.name)

      const dashboardJson = await httpClient.post('/upload', formData)
      .then(response => {
          const jsonData = Object.values(response)[0]

          this.itemsShift = jsonData.filter((rule) => ['Shift'].includes(rule.Category)).map((item, index) => ({
              ...item,
              number: index + 1,
            }));
          this.itemsOvertime = jsonData.filter((rule) => ['Overtime'].includes(rule.Category)).map((item, index) => ({
              ...item,
              number: index + 1,
            }));
          this.itemsRDO = jsonData.filter((rule) => ['RDO'].includes(rule.Category)).map((item, index) => ({
              ...item,
              number: index + 1,
            }));
          this.itemsAllowance = jsonData.filter((rule) => ['Allowance'].includes(rule.Category)).map((item, index) => ({
              ...item,
              number: index + 1,
            }));
          this.itemsLeave = jsonData.filter((rule) => ['Leave'].includes(rule.Category)).map((item, index) => ({
              ...item,
              number: index + 1,
            }));
          this.itemsSuper = jsonData.filter((rule) => ['Super'].includes(rule.Category)).map((item, index) => ({
              ...item,
              number: index + 1,
            }));
          this.itemsMiscellaneous = jsonData.filter
            ((rule) => !['Shift', 'Overtime', 'RDO', 'Allowance', 'Leave', 'Super'].includes(rule.Category)).map((item, index) => ({
              ...item,
              number: index + 1,
            }))
          this.isFileUploaded=true
      })
      .catch(err => {
        //console.log(err);
        //throw err;
        const jsonData = [
                {
                    "Object": "Full Time Day Ordinary Hours",
                    "Category": "Shift",
                    "Rule": "For full time day employees, the span of weekdays is from 07:00 am to 7:00 pm. Maximum ordinary hours per day is 7.6 and per week is 38."
                },
                {
                    "Object": "Full Time Shift Ordinary Hours",
                    "Category": "Shift",
                    "Rule": "For full time shift employees, the span is outside shift. Maximum ordinary hours per day is 7.6 and per week is 38."
                },
                {
                    "Object": "Part Time Ordinary Hours",
                    "Category": "Shift",
                    "Rule": "For part time employees, the span is outside normal part time hours. Maximum ordinary hours is according to part time schedule and maximum per week is 38."
                },
                {
                    "Object": "Casual Day Ordinary Hours",
                    "Category": "Shift",
                    "Rule": "For casual day employees, the span of weekdays is from 7 am to 7 pm. Maximum ordinary hours per day is 10 and per week is 38."
                },
                {
                    "Object": "Casual Shift Ordinary Hours",
                    "Category": "Shift",
                    "Rule": "For casual shift employees, the span is outside shift. Maximum ordinary hours per day is 10 and per week is 38."
                },
                {
                    "Object": "Leave Loading Calculation Logic",
                    "Category": "Leave",
                    "Rule": "Leave loading is calculated as the maximum of 17.5% of base rate or the relevant penalty (night-shift). The base rate is the minimum hourly rate."
                },
                {
                    "Object": "Super Annuation on Annual Leave",
                    "Category": "Super",
                    "Rule": "Super annuation is paid on annual leave for all employment types."
                },
                {
                    "Object": "Super Annuation on Public Holiday Ordinary Hours",
                    "Category": "Super",
                    "Rule": "Super annuation is paid on public holiday ordinary hours for all employment types."
                },
                {
                    "Object": "Super Annuation on Public Holiday Overtime Hours",
                    "Category": "Super",
                    "Rule": "Super annuation is not paid on public holiday overtime hours for all employment types."
                },
                {
                    "Object": "Afternoon Shift Loading and Timing",
                    "Category": "Shift",
                    "Rule": "For all employment types, the afternoon shift loading is 15%. The shift must start after a specified time."
                },
                {
                    "Object": "Night Shift Loading and Timing",
                    "Category": "Shift",
                    "Rule": "For all employment types, the night shift loading is 30%. The shift must start after a specified time and finish before a specified time."
                },
                {
                    "Object": "Permanent Night Shift Loading and Timing",
                    "Category": "Shift",
                    "Rule": "For all employment types, the permanent night shift loading is 30%. The shift must start after a specified time."
                },
                {
                    "Object": "Day Work Shift Loading and Timing",
                    "Category": "Shift",
                    "Rule": "For all employment types, the day work shift loading is 0%. The shift must start after 7:00 AM."
                },
                {
                    "Object": "Full and Part Time Saturday Overtime",
                    "Category": "Overtime",
                    "Rule": "For full and part time employees, Saturday overtime is paid at 200%."
                },
                {
                    "Object": "Casual Saturday Overtime",
                    "Category": "Overtime",
                    "Rule": "For casual employees, Saturday overtime is paid at 225%."
                },
                {
                    "Object": "Full and Part Time Sunday Overtime",
                    "Category": "Overtime",
                    "Rule": "For full and part time employees, Sunday overtime is paid at 200%."
                },
                {
                    "Object": "Casual Sunday Overtime",
                    "Category": "Overtime",
                    "Rule": "For casual employees, Sunday overtime is paid at 225%."
                },
                {
                    "Object": "Full and Part Time Public Holiday Overtime",
                    "Category": "Overtime",
                    "Rule": "For full and part time employees, public holiday overtime is paid at 200%."
                },
                {
                    "Object": "Casual Public Holiday Overtime",
                    "Category": "Overtime",
                    "Rule": "For casual employees, public holiday overtime is paid at 225%."
                },
                {
                    "Object": "All Employment Types Christmas and Good Friday Overtime",
                    "Category": "Overtime",
                    "Rule": "On Christmas or Good Friday, overtime for all employees is paid at 250%."
                },
                {
                    "Object": "Full Time Laundry Allowance",
                    "Category": "Allowance",
                    "Rule": "For full time employees, the laundry allowance is $3.55 per week."
                },
                {
                    "Object": "Part Time and Casual Laundry Allowance",
                    "Category": "Allowance",
                    "Rule": "For part time and casual employees, the laundry allowance is $0.71 per day."
                },
                {
                    "Object": "All Employment Types Meal Allowance",
                    "Category": "Allowance",
                    "Rule": "For all employees, the meal allowance is $16.91 if overtime is greater than 1.5 hours and an additional $13.54 if overtime is greater than 4 hours."
                },
                {
                    "Object": "First Aid Allowance",
                    "Category": "Allowance",
                    "Rule": "For all employees with first aid duties, the first aid allowance is $14.11 weekly."
                }
            ]

            this.itemsShift = jsonData.filter((rule) => ['Shift'].includes(rule.Category)).map((item, index) => ({
              ...item,
              number: index + 1,
            }));
          this.itemsOvertime = jsonData.filter((rule) => ['Overtime'].includes(rule.Category)).map((item, index) => ({
              ...item,
              number: index + 1,
            }));
          this.itemsRDO = jsonData.filter((rule) => ['RDO'].includes(rule.Category)).map((item, index) => ({
              ...item,
              number: index + 1,
            }));
          this.itemsAllowance = jsonData.filter((rule) => ['Allowance'].includes(rule.Category)).map((item, index) => ({
              ...item,
              number: index + 1,
            }));
          this.itemsLeave = jsonData.filter((rule) => ['Leave'].includes(rule.Category)).map((item, index) => ({
              ...item,
              number: index + 1,
            }));
          this.itemsSuper = jsonData.filter((rule) => ['Super'].includes(rule.Category)).map((item, index) => ({
              ...item,
              number: index + 1,
            }));
          this.itemsMiscellaneous = jsonData.filter
            ((rule) => !['Shift', 'Overtime', 'RDO', 'Allowance', 'Leave', 'Super'].includes(rule.Category)).map((item, index) => ({
              ...item,
              number: index + 1,
            }))
          this.isFileUploaded=true
      })
      .finally(() =>{
        loadingService.showLoading(false);
      })
    },
    handleReviewButtonClick(){
      console.log('clicked')
    },
    handleFinalButtonClick() {
      console.log(" ENTERED")
        this.isModalVisible=true;
        console.log(" ENTERED 1111:", this.isModalVisible)
    },
    closeModal() {
        this.isModalVisible = false;
      },
  },
}
</script>

<style lang="scss" scoped>

.custom-file-input-label {
  cursor: pointer;
  display: inline-block;
}

.button-image {
  max-width: 100%;
  height: auto;
}

.va-card-style {
  overflow-x: auto;
  background-color: #eeeeee;
  color: white;
}

.va-card-style-internal {
  overflow-x: auto;
  color: black;
}

#main-container {
  background-size: auto;
  color: black;
}

.modal-overlay {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}

.modal {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
}

.modal-add {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  min-width: 400px;
  min-height: 400px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
}

.modal-confirm {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  min-width: 200px;
  min-height: 200px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
}

.form-row {
  display: flex;
  flex-direction: column;
  margin-bottom: 10px;
}

.loader-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* Adjust to your needs */
}

.loader {
  border: 4px solid red; /* Loader color */
  border-top: 4px solid transparent;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.input-s {
  width: 250px;
  height: 2rem;
}
</style>
