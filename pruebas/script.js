import http from 'k6/http';
import { sleep, check } from 'k6';

export const options = {
  stages: [
    { duration: '60s', target: 30 }, 
  ],
};

export default function () {
  const url = 'http://localhost:8000/pedidos';
  const payload = JSON.stringify({
    producto: 'Sensor IoT',
    cantidad: Math.floor(Math.random() * 5) + 1
  });
  
  const params = {
    headers: { 'Content-Type': 'application/json' },
  };

  const res = http.post(url, payload, params);
  
  check(res, {
    'status es 201': (r) => r.status === 201,
  });
  
  sleep(1);
}