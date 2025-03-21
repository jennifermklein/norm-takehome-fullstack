import { Box, Divider, List, ListItem, Text } from '@chakra-ui/react';

export interface Citation {
  source: string;
  text: string;
}

export default function CitationList({ citations }: { citations: Citation[] }) {
  return (
    <>
      <Divider />
      <Box>
        <Text fontWeight="bold" fontSize="lg" mb={2}>
          Citations:
        </Text>
        <List as="ol">
          {citations.map((citation, i) => (
            <ListItem key={`${i}-${citation.source}`}>
              <Box>
                <Text>
                  <Text as="span" fontWeight="bold">
                    [{i + 1}] {citation.source}
                  </Text>
                  {' - '}
                  {citation.text}
                </Text>
              </Box>
            </ListItem>
          ))}
        </List>
      </Box>
    </>
  );
}
