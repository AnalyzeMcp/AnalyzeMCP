import React, { useState, useEffect } from 'react';
import { Box, Card, CardContent, Typography, Grid } from '@mui/material';

interface AnalyzerProps {
  data: {
    protocol_type: string;
    packet_size: number;
    timestamp: string;
  }[];
}

const ProtocolAnalyzer: React.FC<AnalyzerProps> = ({ data }) => {
  const [stats, setStats] = useState({
    totalPackets: 0,
    averageSize: 0,
    protocolDistribution: {} as Record<string, number>
  });

  useEffect(() => {
    if (data.length === 0) return;

    // Calculate statistics
    const totalPackets = data.length;
    const averageSize = data.reduce((acc, curr) => acc + curr.packet_size, 0) / totalPackets;
    
    // Calculate protocol distribution
    const distribution = data.reduce((acc, curr) => {
      acc[curr.protocol_type] = (acc[curr.protocol_type] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    setStats({
      totalPackets,
      averageSize,
      protocolDistribution: distribution
    });
  }, [data]);

  return (
    <Box sx={{ flexGrow: 1, p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Protocol Analysis
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Packets
              </Typography>
              <Typography variant="h4">
                {stats.totalPackets}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Average Packet Size
              </Typography>
              <Typography variant="h4">
                {stats.averageSize.toFixed(2)} bytes
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Protocol Distribution
              </Typography>
              {Object.entries(stats.protocolDistribution).map(([protocol, count]) => (
                <Box key={protocol} sx={{ mt: 2 }}>
                  <Typography variant="subtitle1">
                    {protocol}: {count} packets
                  </Typography>
                </Box>
              ))}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ProtocolAnalyzer;