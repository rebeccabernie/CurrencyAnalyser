<script>
/* http://vue-chartjs.org/#/home?id=reactive-data
   Extend Line component from the vue-chartjs plugin, and add the reactive prop mixen.
   The reactive prop mixen adds a watcher function that allows the continuous update of data (both chart data and labels) while also scaling the graph accordingly.
*/
import { Line, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

export default {
  extends: Line,
  mixins: [reactiveProp],
  props: ['options'],
  mounted () {
    // this.chartData is created in the mixin.
    this.renderChart(this.chartData, this.options)
  }
}
</script>