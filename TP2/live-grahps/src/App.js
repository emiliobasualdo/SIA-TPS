import {Chart} from "react-google-charts"
import {Component} from "react"
import { w3cwebsocket as W3CWebSocket } from "websocket";

const client = new W3CWebSocket('ws://127.0.0.1:8080');
class App extends Component{
  constructor(props) {
    super(props)
    this.state = {fit:[], count:[]}
  }
  
  componentWillMount() {
    client.onopen = () => {
      console.log('WebSocket Client Connected');
    };
    client.onmessage = (message) => {
      const new_Data = JSON.parse(message.data);
      this.setState({
        fit:[...this.state.fit, new_Data.slice(0,4)],
        count:[...this.state.count, [new_Data[0], new_Data[4]]],
      })
    };
  }
  render() {
    return (
      <div>
        <Chart
          width={'600px'}
          height={'400px'}
          chartType="LineChart"
          loader={<div>Loading Chart</div>}
          data={[
            ['Iteraciones', 'Min', 'Avg', "Max"],
            ...this.state.fit
          ]}
          options={{
            title: 'Min., Avg. y Max Fitness',
            hAxis: { title: 'Iteraciones', minValue: 0, maxValue:500},
            vAxis: { title: 'Fitness', minValue: 0},
          }}
          rootProps={{ 'data-testid': '1' }}
          legendToggle
        />
        
        <Chart
          width={'600px'}
          height={'400px'}
          chartType="LineChart"
          loader={<div>Loading Chart</div>}
          data={[
            ['Iteraciones', 'Count'],
            ...this.state.count
          ]}
          options={{
            title: 'Cantidad de agentes',
            hAxis: { title: 'Iteraciones', minValue: 0, maxValue: 1000 },
            vAxis: { title: 'Count', minValue: 0, maxValue: 1000 },
          }}
          rootProps={{ 'data-testid': '1' }}
          legendToggle
        />
      </div>
    );
  }
}

export default App;
