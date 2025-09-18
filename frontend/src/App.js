import { useState, useEffect, useMemo } from 'react';
import { 
  AppBar, Toolbar, Typography, Container, Grid, Card, 
  CardContent, CircularProgress, Box, Chip, Link, Tabs, Tab, Tooltip,
  ToggleButton, ToggleButtonGroup, Divider, Select, MenuItem, FormControl, InputLabel
} from '@mui/material';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import VerifiedUserIcon from '@mui/icons-material/VerifiedUser';
import { formatDistanceToNow } from 'date-fns';
import SentimentBar from './SentimentBar';

// The professionalTheme definition remains the same
const professionalTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#00b0ff' },
    background: { default: 'transparent', paper: 'rgba(255, 255, 255, 0.05)' },
    success: { main: '#00e676' },
    warning: { main: '#ffc400' },
    error: { main: '#ff3d00' },
  },
  typography: { fontFamily: 'Roboto, Arial, sans-serif' },
  components: {
    MuiCard: { styleOverrides: { root: { backdropFilter: 'blur(12px)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '12px' } } },
    MuiChip: { styleOverrides: { root: { fontWeight: 'bold' } } },
  },
});

const CATEGORIES = ["Tech", "Automobile", "Oil & Gas", "Finance"];

function App() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState(CATEGORIES[0]);
  const [sortOrder, setSortOrder] = useState('relevant');
  const [selectedEvent, setSelectedEvent] = useState('All');

  useEffect(() => {
    const fetchArticles = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(`http://127.0.0.1:5001/api/news/category/${selectedCategory}`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const data = await response.json();
        setArticles(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchArticles();
  }, [selectedCategory]);

  const eventTypes = useMemo(() => {
    return ['All', ...new Set(articles.map(article => article.event_type))];
  }, [articles]);

  const filteredAndSortedArticles = useMemo(() => {
    return articles
      .filter(article => selectedEvent === 'All' || article.event_type === selectedEvent)
      .sort((a, b) => {
        if (sortOrder === 'newest') return b.datetime - a.datetime;
        return b.is_trusted_source - a.is_trusted_source;
      });
  }, [articles, sortOrder, selectedEvent]);

  return (
    <ThemeProvider theme={professionalTheme}>
      <CssBaseline />
      <AppBar position="static" color="transparent" elevation={0} sx={{ borderBottom: '1px solid rgba(255, 255, 255, 0.1)' }}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 'bold' }}>Market Sentiment Dashboard</Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center" flexWrap="wrap" mb={3} gap={2}>
          <Tabs value={selectedCategory} onChange={(e, v) => setSelectedCategory(v)}>
            {CATEGORIES.map(c => <Tab label={c} value={c} key={c} />)}
          </Tabs>
          <Box display="flex" gap={2} alignItems="center">
            <FormControl size="small" sx={{ minWidth: 180 }}>
              <InputLabel>Event Type</InputLabel>
              <Select value={selectedEvent} label="Event Type" onChange={(e) => setSelectedEvent(e.target.value)}>
                {eventTypes.map(type => <MenuItem key={type} value={type}>{type}</MenuItem>)}
              </Select>
            </FormControl>
            <ToggleButtonGroup value={sortOrder} exclusive onChange={(e, v) => v && setSortOrder(v)}>
              <ToggleButton value="relevant">Relevant</ToggleButton>
              <ToggleButton value="newest">Newest</ToggleButton>
            </ToggleButtonGroup>
          </Box>
        </Box>

        {loading ? (
          <Box display="flex" justifyContent="center" minHeight="60vh"><CircularProgress /></Box>
        ) : error ? (
          <Typography color="error" align="center">{error}</Typography>
        ) : (
          <Grid container spacing={4}>
            {filteredAndSortedArticles.map((article) => (
              <Grid item xs={12} sm={6} md={4} key={article.id}>
                <Card sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
                  <CardContent sx={{ flexGrow: 1 }}>
                    <Box display="flex" justifyContent="space-between" alignItems="center" mb={1.5}>
                      <Chip 
                        label={article.ticker_price ? `${article.ticker}: $${article.ticker_price.toFixed(2)}` : article.ticker}
                        size="small" 
                        variant="outlined" 
                      />
                      <Typography variant="caption" color="text.secondary">
                        {formatDistanceToNow(new Date(article.datetime * 1000), { addSuffix: true })}
                      </Typography>
                    </Box>
                    <Typography gutterBottom variant="h5" component="h2" sx={{ fontWeight: 'bold' }}>{article.headline}</Typography>
                    <Chip label={article.event_type} size="small" color="secondary" variant="filled" sx={{ mb: 1.5 }} />
                    <SentimentBar sentiment={article.sentiment} />
                  </CardContent>
                  
                  {/* --- THIS SECTION IS NOW FIXED --- */}
                  {article.mentioned_stocks && article.mentioned_stocks.length > 0 && (
                    <Box sx={{ px: 2, pb: 2 }}>
                      <Divider sx={{ my: 1 }} />
                      <Typography variant="subtitle2" sx={{ mb: 1 }}>Mentioned Stocks:</Typography>
                      <Box display="flex" flexWrap="wrap" gap={1}>
                        {article.mentioned_stocks.map(stock => (
                          <Chip key={stock.ticker} label={`${stock.ticker}: $${stock.price.toFixed(2)}`} size="small" />
                        ))}
                      </Box>
                    </Box>
                  )}
                  
                  {/* --- THIS SECTION IS ALSO FIXED --- */}
                  <Box sx={{ p: 2, pt: 1, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Box>
                      {article.is_trusted_source && <Chip icon={<VerifiedUserIcon />} label="Trusted" size="small" color="primary" />}
                    </Box>
                    <Link href={article.url} target="_blank" rel="noopener noreferrer" sx={{ fontWeight: 'bold' }}>Read Article</Link>
                  </Box>
                </Card>
              </Grid>
            ))}
          </Grid>
        )}
      </Container>
    </ThemeProvider>
  );
}

export default App;