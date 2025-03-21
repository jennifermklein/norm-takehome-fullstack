'use client';

import HeaderNav from '@/components/HeaderNav';
import QueryUI from '@/components/QueryUI';

export default function Page() {
  return (
    <>
      <HeaderNav signOut={() => {}} />
      <QueryUI />
    </>
  );
}
