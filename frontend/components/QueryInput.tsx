import { Stack, Textarea, Button } from '@chakra-ui/react';

export default function QueryInput({
  queryText,
  setQueryText,
  submitQuery,
  loading,
}: {
  queryText: string;
  setQueryText: (text: string) => void;
  submitQuery: () => void;
  loading: boolean;
}) {
  return (
    <Stack spacing={2} alignItems="flex-start">
      <Textarea
        width="xl"
        variant="filled"
        placeholder="Ask a question about the laws of Westeros..."
        value={queryText}
        onChange={(e) => setQueryText(e.target.value)}
      />
      <Button
        type="submit"
        variant="ghost"
        colorScheme="purple"
        alignSelf="flex-end"
        onClick={submitQuery}
        disabled={loading}
      >
        Submit
      </Button>
    </Stack>
  );
}
