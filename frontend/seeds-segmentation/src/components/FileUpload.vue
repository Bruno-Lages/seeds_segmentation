
<script setup>
	import { ref, defineEmits } from 'vue';
	
	const emit = defineEmits(['imageUploaded', 'inferSuccess']);
	
	const fileInput = ref(null);
	const imageUrl = ref(null);

	const API_URL = import.meta.env.VITE_API_URL

	async function uploadImage(file) {
		const formData = new FormData();
		formData.append('file', file);

		try {
			const response = await fetch(API_URL + "infer", {
			method: 'POST',
			body: formData,
			});

			const data = await response.json();
			console.log('Upload Success:', data);

			emit('inferSuccess', data);
		} catch (error) {
			console.error('Upload Failed:', error);
		}
	};
	

	async function handleFileUpload(event) {
		const file = event.target.files[0];
		if (file) {
			imageUrl.value = URL.createObjectURL(file);
			emit('imageUploaded', imageUrl.value);
			
			await uploadImage(file);
		}
	};
	
	async function handleDrop (event) {
		event.preventDefault();
		const file = event.dataTransfer.files[0];
		if (file) {
			imageUrl.value = URL.createObjectURL(file);
			emit('imageUploaded', imageUrl.value);
			
			await uploadImage(file);
		}
	};
	
	const triggerFileInput = () => {
		fileInput.value.click();
	};
</script>

<template>
    <div 
      class="upload-box" 
      @dragover.prevent 
      @drop="handleDrop" 
      @click="triggerFileInput"
    >
      
		<input type="file" 
		ref="fileInput" 
		@change="handleFileUpload" 
		hidden 
		accept="image/*"  />
		
		<img v-if="imageUrl" :src="imageUrl" class="uploaded-image" />
		
		<div v-else class="upload-placeholder">
			Drop or Click to Upload
		</div>
    </div>
</template>

<style scoped>
  .upload-box {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    border: 2px dashed #aaa;
    position: relative;
  }
  
  .upload-placeholder {
    font-size: 16px;
    color: #666;
  }
  
  .uploaded-image {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }
  </style>
  