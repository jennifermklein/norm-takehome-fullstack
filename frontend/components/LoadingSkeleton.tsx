import { Box, Skeleton, Stack } from '@chakra-ui/react';

export default function LoadingSkeleton() {
  return (
    <Stack spacing={4} w="xl">
      <Box>
        <Skeleton height="20px" width="20%" mb={2} />
        <Skeleton height="20px" width="100%" mb={2} />
        <Skeleton height="20px" width="100%" mb={2} />
        <Skeleton height="20px" width="100%" mb={2} />
        <Skeleton height="20px" width="100%" />
      </Box>
    </Stack>
  );
}
