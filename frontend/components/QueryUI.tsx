import { useState } from 'react';
import { Box, Flex, Stack, Text, Alert, AlertIcon } from '@chakra-ui/react';
import QueryInput from './QueryInput';
import LoadingSkeleton from './LoadingSkeleton';
import CitationList, { Citation } from './CitationList';

export default function QueryBox() {
  const [queryText, setQueryText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState('');
  const [citations, setCitations] = useState<Citation[]>([]);

  const submitQuery = async () => {
    // reset any responses from previous queries
    setError('');
    setQuestion('');
    setResponse('');
    setCitations([]);

    if (queryText.trim() === '') {
      setError('Please enter a query');
      return;
    }

    const url = `http://localhost:8000/laws/query?query=${queryText}`;
    try {
      setLoading(true);
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        setError(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // update state with new response
      setQuestion(data.query);
      setResponse(data.response);
      setCitations(data.citations);
      setQueryText('');
    } catch (error) {
      setError(`Error: ${error}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Flex
      direction="column"
      justifyContent="center"
      alignItems="center"
      h="100vh"
    >
      <QueryInput
        queryText={queryText}
        setQueryText={setQueryText}
        submitQuery={submitQuery}
        loading={loading}
      />
      {loading && <LoadingSkeleton />}
      <Stack spacing={2} alignItems="flex-start" w="xl">
        {error && (
          <Alert status="error">
            <AlertIcon />
            {error}
          </Alert>
        )}
        {question && (
          <Box>
            <Text fontWeight="bold" fontSize="lg" mb={2}>
              Your question:
            </Text>
            <Text>{question}</Text>
          </Box>
        )}
        {/* the citation numbers might not be in order, should update the backend to fix this in sync with the citation list */}
        {response && (
          <Box>
            <Text fontWeight="bold" fontSize="lg" mb={2}>
              Response:
            </Text>
            <Text>{response}</Text>
          </Box>
        )}
        {/* for now all citations are shown, should consider filtering out uncited citations */}
        {citations.length && <CitationList citations={citations} />}
      </Stack>
    </Flex>
  );
}
