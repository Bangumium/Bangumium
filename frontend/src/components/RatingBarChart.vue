<template>
  <div ref="chart"
    style="width: 100%; height: 200px; border-radius: 20px;margin-top: 20px; border: 2px solid oklch(var(--s));"></div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import * as echarts from "echarts";

const props = defineProps({
  chartData: {
    type: Array,
    required: true,
  }
});

const chart = ref(null);

onMounted(() => {
  initChart();
});

const initChart = () => {
  const chartInstance = echarts.init(chart.value, {
    'color': ['#FFC0CB'],
  }, { renderer: 'svg' });
  const option = {
    xAxis: {
      type: 'category',
      data: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
    },
    yAxis: {
      show: false
    },
    series: [{
      data: props.chartData,
      type: 'bar',
      label: {
        show: true,
        position: 'top',
        color: '#cc0099',
        formatter: '{c}',
      },
    }],
    height: '100px',
  };
  chartInstance.setOption(option);
};
</script>

<style scoped></style>
