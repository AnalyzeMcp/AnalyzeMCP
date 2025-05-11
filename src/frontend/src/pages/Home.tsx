import React, { useState } from 'react';
import { Container, Grid, Paper } from '@mui/material';
import Dashboard from '../components/Dashboard';
import ProtocolAnalyzer from '../components/ProtocolAnalyzer';

const Home: React.FC = () => {
  const [protocolData] = useState([
    {
      protocol_type: 'MCP-1',
      packet_size: 100,
      timestamp: new Date().toISOString(),
    },
    {
      protocol_type: 'MCP-2',
      packet_size: 150,
      timestamp: new Date().toISOString(),
    },
  ]);

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
            <Dashboard />
          </Paper>
        </Grid>
        <Grid item xs={12}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
            <ProtocolAnalyzer data={protocolData} />
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Home;