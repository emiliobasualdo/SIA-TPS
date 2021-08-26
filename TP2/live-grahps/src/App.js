import {Chart} from "react-google-charts"
import {Component} from "react"
import { w3cwebsocket as W3CWebSocket } from "websocket";

const client = new W3CWebSocket('ws://127.0.0.1:8080');
class App extends Component{
  constructor(props) {
    super(props)
    this.state = {data:[]}
  }
  
  componentWillMount() {
    client.onopen = () => {
      console.log('WebSocket Client Connected');
    };
    client.onmessage = (message) => {
      const data = JSON.parse(message.data);
      this.setState({data:data})
    };
  }
  render() {
    return (
      <Chart
        width={'600px'}
        height={'400px'}
        chartType="LineChart"
        loader={<div>Loading Chart</div>}
        data={[
          ['Iteraciones', 'Min Fitness', 'Avg Fitness'],
          ...this.state.data
        ]}
        options={{
          title: 'Min. y Avg. Fitness',
          hAxis: { title: 'Iteraciones', minValue: 0, maxValue: 1000 },
          vAxis: { title: 'Fitness', minValue: 0, maxValue: 600 },
          legend: 'none',
        }}
        rootProps={{ 'data-testid': '1' }}
      />
    );
  }
}

export default App;
