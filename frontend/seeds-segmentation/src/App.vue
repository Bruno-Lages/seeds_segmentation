<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import BaseSquare  from './components/BaseSquare.vue';
import FileUpload from './components/FileUpload.vue';
import PointCanvas from './components/PointCanvas.vue';

const API_URL = import.meta.env.VITE_API_URL

const currentHour = ref('');

const imageUrl = ref(null);

const svgWidth = ref(0);
const svgHeight = ref(0);

const coordinates = ref([]);
const area = ref(null);


function handleImageUpload(url) {
  imageUrl.value = url;
};

async function updateSvgSize() {
	const img = new Image();
	img.src = imageUrl.value;
	
	img.onload = () => {
		svgWidth.value = img.width;
		svgHeight.value = img.height;
	};
};

async function getArea(instances) {
    try {
        const response = await fetch(API_URL + "area", {
        	method: 'POST',
			headers: {
                'Content-Type': 'application/json'
            },
        	body: JSON.stringify({ instances }),
        });

        const data = await response.json();

		area.value = data.total_area
    } catch (error) {
        console.error('Upload Failed:', error);
    }
};

async function handleInfer(data) {
	coordinates.value = data.instances;
	await updateSvgSize();
	await getArea(data.instances);
}

function updateCurrentTime() {
	const now = new Date();
	currentHour.value = now.toLocaleTimeString([], { 
		hour: '2-digit', 
		minute: '2-digit' 
	});
};

onMounted(() => {
	updateCurrentTime();
	const timeInterval = setInterval(updateCurrentTime, 1000);

	onBeforeUnmount(() => {
		clearInterval(timeInterval);
	});
});

</script>

<template>
	<header>
		<img alt="TCX logo" src="./assets/tcx.png" width="125" height="125" />

		<span class="time">{{ currentHour }}</span>

	</header>

	<main>
		<BaseSquare title="Uploaded Image">
			<FileUpload @imageUploaded="handleImageUpload" @inferSuccess="handleInfer" />
		</BaseSquare>

		<div>
			<BaseSquare title="Segmented Image">
				
		<PointCanvas 
		v-if="imageUrl" 
		:coordinates="coordinates"  
		:svgWidth="svgWidth"
		:svgHeight="svgHeight"/>

				<span v-else>No image selected</span>
			</BaseSquare>
			<span v-if="area">Total Area: {{ area}} px</span>
		</div>
	</main>
</template>

<style scoped>
header {
	width: 100%;
	line-height: 1.5;
	display: flex;
	justify-content: space-between;
	align-items: center;
}

.time {
	padding: 1.5rem;
	margin: auto 0;
}

main {
	display: flex;
	justify-content: space-around;
	width: 100%;
}

@media (max-width: 1024px) {
	header {
		display: flex;
		place-items: center;
		padding-right: calc(var(--section-gap) / 2);
	}

	main {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
	}
}
</style>
