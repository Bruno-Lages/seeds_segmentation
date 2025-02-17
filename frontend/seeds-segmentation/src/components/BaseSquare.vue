<script setup>
defineProps({
  	title: String
});
</script>

<template>
	<div class="base-container">
		<h2>{{ title }}</h2>
		<div class="square-block">
		<slot>

		</slot>
		</div>
	</div>
</template>

<style scoped>
.base-container {
  	text-align: center;
}

.square-block {
	width: 300px;
	height: 300px;
	border: 2px solid #aaa;
	display: flex;
	align-items: center;
	justify-content: center;
	position: relative;
	overflow: hidden;
}
</style>
