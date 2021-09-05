import {Chart} from "react-google-charts"
import { Container, Col, Row } from 'react-bootstrap';
import {Component} from "react"
import { w3cwebsocket as W3CWebSocket } from "websocket";

const client = new W3CWebSocket('ws://127.0.0.1:8080');
class App extends Component{
  constructor(props) {
    super(props)
    this.state = {fitness:[], height:[], diversity:[]}
  }
  
  componentWillMount() {
    client.onopen = () => {
      console.log('WebSocket Client Connected');
    };
    client.onmessage = (message) => {
      const new_Data = JSON.parse(message.data);
      this.setState({
        fitness:[...this.state.fitness, new_Data[0]],
        height:[...this.state.height, new_Data[1]],
        diversity:[...this.state.diversity, new_Data[2]],
      })
    };
  }
  render() {
    return (
      <Container>
        <Row>
          <Col>
            <Chart
              width={'900px'}
              chartType="LineChart"
              loader={<div>Loading Chart</div>}
              data={[
                ['Generation', 'Min', 'Avg', "Max"],
                ...this.state.fitness
              ]}
              options={{
                title: 'Min., Avg. y Max Fitness',
                hAxis: { title: 'Generation', minValue: 0, maxValue:500},
                vAxis: { title: 'Fitness', minValue: 0},
              }}
              rootProps={{ 'data-testid': '1' }}
              legendToggle
            />
          </Col>
          <Col>
            <Chart
              width={'900px'}
              chartType="LineChart"
              loader={<div>Loading Chart</div>}
              data={[
                ['Generation', 'Min', 'Avg', "Max"],
                ...this.state.height
              ]}
              options={{
                title: 'Min., Avg. y Max Height',
                hAxis: { title: 'Generation', minValue: 0, maxValue:500},
                vAxis: { title: 'Height', minValue: 0, maxValue:2.1 },
              }}
              rootProps={{ 'data-testid': '1' }}
              legendToggle
            />
          </Col>
        </Row>
        <Row>
          <Col>
            <Chart
              width={'900px'}
              chartType="LineChart"
              loader={<div>Loading Chart</div>}
              data={[
                ['Generation', "armas", "botas", "cascos", "guantes", "pecheras", "height"],
                ...this.state.diversity
              ]}
              options={{
                title: 'Diversidad: Alelos por Locus',
                hAxis: { title: 'Generation', minValue: 0, maxValue:500},
                vAxis: { title: 'Alelos por Locus', minValue: 0},
              }}
              rootProps={{ 'data-testid': '1' }}
              legendToggle
            />
          </Col>
        </Row>
      </Container>
    );
  }
}

export default App;
