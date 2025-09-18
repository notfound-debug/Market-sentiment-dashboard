import React from 'react';
import Box from '@mui/material/Box';
import Tooltip from '@mui/material/Tooltip';

const SentimentBar = ({ sentiment }) => {
  const { positive, neutral, negative } = sentiment;
  const total = positive + neutral + negative;

  // Handle the case where total might be 0 to avoid division by zero
  if (total === 0) {
    return <Box sx={{ display: 'flex', height: '10px', borderRadius: '5px', overflow: 'hidden', backgroundColor: '#424242' }} />;
  }

  const posPercent = (positive / total) * 100;
  const neuPercent = (neutral / total) * 100;
  const negPercent = (negative / total) * 100;

  return (
    <Box sx={{ display: 'flex', height: '8px', borderRadius: '4px', overflow: 'hidden', width: '100%', my: 1.5 }}>
      <Tooltip title={`Positive: ${posPercent.toFixed(1)}%`} placement="top">
        <Box sx={{ width: `${posPercent}%`, backgroundColor: 'success.main' }} />
      </Tooltip>
      <Tooltip title={`Neutral: ${neuPercent.toFixed(1)}%`} placement="top">
        <Box sx={{ width: `${neuPercent}%`, backgroundColor: 'warning.main' }} />
      </Tooltip>
      <Tooltip title={`Negative: ${negPercent.toFixed(1)}%`} placement="top">
        <Box sx={{ width: `${negPercent}%`, backgroundColor: 'error.main' }} />
      </Tooltip>
    </Box>
  );
};

export default SentimentBar;