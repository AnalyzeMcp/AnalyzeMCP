import React from 'react';
import { Box, Grid, Paper, Typography, useTheme } from '@mui/material';
import { ResponsiveLine } from '@nivo/line';
import { ResponsiveBar } from '@nivo/bar';

interface AnalysisData {
  title: string;
  value: number;
  change: number;
  data: Array<{ x: string; y: number }>;
}

interface DashboardProps {
  data: {
    analysis: AnalysisData[];
    insights: string[];
    recommendations: string[];
  };
}

const Dashboard: React.FC<DashboardProps> = ({ data }) => {
  const theme = useTheme();

  const MetricCard = ({ title, value, change, data }: AnalysisData) => (
    <Paper
      sx={{
        p: 2,
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <Typography variant="h6" gutterBottom>
        {title}
      </Typography>
      <Typography variant="h4" component="div">
        {value}
      </Typography>
      <Typography
        variant="body2"
        color={change >= 0 ? 'success.main' : 'error.main'}
      >
        {change >= 0 ? '+' : ''}{change}%
      </Typography>
      <Box sx={{ height: 100, mt: 2 }}>
        <ResponsiveLine
          data={[{ id: title, data: data }]}
          margin={{ top: 10, right: 10, bottom: 10, left: 10 }}
          xScale={{ type: 'point' }}
          yScale={{ type: 'linear', min: 'auto', max: 'auto' }}
          curve="monotoneX"
          enablePoints={false}
          enableGridX={false}
          enableGridY={false}
          axisTop={null}
          axisRight={null}
          axisBottom={null}
          axisLeft={null}
          colors={{ scheme: 'nivo' }}
          theme={{
            axis: { ticks: { text: { fontSize: 10 } } },
            grid: { line: { stroke: theme.palette.divider } },
          }}
        />
      </Box>
    </Paper>
  );

  return (
    <Box sx={{ flexGrow: 1, p: 3 }}>
      <Grid container spacing={3}>
        {/* Metrics */}
        {data.analysis.map((metric, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <MetricCard {...metric} />
          </Grid>
        ))}

        {/* Insights */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Key Insights
            </Typography>
            <Box component="ul" sx={{ mt: 2, pl: 2 }}>
              {data.insights.map((insight, index) => (
                <Typography
                  component="li"
                  variant="body1"
                  key={index}
                  sx={{ mb: 1 }}
                >
                  {insight}
                </Typography>
              ))}
            </Box>
          </Paper>
        </Grid>

        {/* Recommendations */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Recommendations
            </Typography>
            <Box component="ul" sx={{ mt: 2, pl: 2 }}>
              {data.recommendations.map((recommendation, index) => (
                <Typography
                  component="li"
                  variant="body1"
                  key={index}
                  sx={{ mb: 1 }}
                >
                  {recommendation}
                </Typography>
              ))}
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;