import { useWeb3React } from '@web3-react/core';
import { useEffect } from 'react';

export default function submit() {
    function joinQueue(data?: Array<number>) {
        // const { isActive, chainId, account, provider } = useWeb3React();
        console.log(data);
    }

    return { joinQueue };
}
