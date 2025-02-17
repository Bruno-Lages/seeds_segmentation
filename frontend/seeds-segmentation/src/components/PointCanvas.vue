<script setup>
import { computed } from 'vue';

const props = defineProps({
	coordinates: {
		type: Array,
		default: () => []
	},
	svgWidth: {
		type: Number,
		required: true,
	},
	svgHeight: {
		type: Number,
		required: true,
	}
});

const viewBox = computed(() => `0 0 ${props.svgWidth} ${props.svgHeight}`);

</script>

<template>
	<svg 
	:width="svgWidth" 
	:height="svgHeight"
	:viewBox="viewBox"
	class="point-overlay">
		<polygon
		v-for="(instance, index) in coordinates"
		:key="index"
		:points="instance.map(point => `${point.x},${point.y}`).join(' ')"
		fill="white"
		stroke="white"
		stroke-width="0.5"
		/>
	</svg>
</template>

<style scoped>
.point-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>
