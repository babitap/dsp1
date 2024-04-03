<template>
  <div class="file-uploader">
    <label for="fileInput" class="custom-file-input-label">
      <img src="@/assets/img/transparent_upload_logo.png" alt="Upload Image" class="button-image" />
    </label>
    <input
      type="file"
      id="fileInput"
      ref="fileInput"
      style="display: none;"
      @change="$emit('change', $event)"
    />
    <div style="margin-left: 8rem;">
       <h2>Upload your award documents(s)</h2>
    </div>
  </div>
</template>

<style scoped>
.file-uploader {
  margin: 1rem;
}

.custom-file-input-label {
  cursor: pointer;
  display: inline-block;
}

.button-image {
  max-width: 100%;
  height: auto;
}
</style>
