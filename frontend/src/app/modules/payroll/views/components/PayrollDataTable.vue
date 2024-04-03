<template>
  <va-data-table :data="items" :fields="fields" class="elevation-1">
    <template slot="actions" slot-scope="props">
      <va-button medium style="width: 150px;" @click="editRow(props.rowData)">Edit Rule</va-button>
      <va-button medium style="width: 150px;" @click="removeRow(props.rowData)">Delete Rule</va-button>
      <va-button medium style="width: 150px;" @click="editRow(props.rowData)">Add Comment</va-button>
    </template>
  </va-data-table>
</template>

<script>
export default {
  data() {   
    return {
      isChecked: false,
      editedItem: {},
      showConfirmationDialog: false,
      showSaveConfirmationDialog: false,
      showEditDialog: false, 
      isCheckedArray: new Array(this.items.length).fill(false),     
    };
  },
 
  props: {
    items: {
      type: Array,
      required: true, 
    },
    fields: {
      type: Array,
      required: true,     
    },
   // isCheckedArray: Array,
  },
  computed: {
    visibleFields() {     
      return this.fields.slice(0, 5);
    },
  },  
  methods: {
    editingItem(item) {      
      this.showEditDialog = true;   
      this.editedItem = { ...item };      
    },   
    closeConfirmModal()
    {
      this.showConfirmationDialog = false;
    },
    toggleCheckbox(index) {
      this.$set(this.isCheckedArray, index, !this.isCheckedArray[index]);
    },
    saveConfirmModal(){
      this.showSaveConfirmationDialog = true;
      this.showConfirmationDialog = false;
    },
    closeSaveConfirmModal(){
      this.showSaveConfirmationDialog = false;
      this.showEditDialog = false;
    },
    closeDialog() {
      this.showEditDialog = false;
    },
    updateItem(item) {      
      const index = this.items.indexOf(item);
      this.$set(this.items, index, { ...item }); 
      this.editedItem = {};
      this.showConfirmationDialog = true;
      closeDialog() 
    },
    deleteItem(item) {
      // Add delete logic
      this.showConfirmationDialog = true;
      console.log("Delete comment for item:", item);
    },
  },
  methods: {
    removeRow(item) {
      // Find the index of the item in the items array
      const index = this.items.indexOf(item);

      // Remove the item from the array
      if (index !== -1) {
        this.items.splice(index, 1);
      }
    },
    editRow(itemData) {
      this.$emit("editRule",itemData)
    },
  },
  methods: {
    removeRow(item) {
      // Find the index of the item in the items array
      const index = this.items.indexOf(item);

      // Remove the item from the array
      if (index !== -1) {
        this.items.splice(index, 1);
      }
    },
    editRow(itemData) {
      this.$emit("editRule",itemData)
    },
  },
};
</script>

<style lang="scss" scoped>
.v-data-table .v-data-table-header th {
  font-size: 100px; /* You can adjust the font size to your preference */
}

.popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  z-index: 999;
}

.vertical-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-bottom: 1rem;
}

.icon-row {
  display: flex;
  gap: 10px; /* Adjust the gap as needed */
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
  min-width: 400px;
  min-height: 400px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
}

.modal-info {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  min-width: 200px;
  min-height: 200px;
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
  margin-bottom: 10px; /* Adjust the margin as needed */
}

.input-s {
  width: 250px;
  height: 2rem;
}

.va-table th,
.content table th {
  font-size: 1rem;
}

.label-s {
  text-align: left;
  font-size: medium;
  font-weight: bold;
  text-transform: uppercase;
}
</style>
