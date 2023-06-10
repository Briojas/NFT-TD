import type { AddEthereumChainParameter } from '@web3-react/types';

const ETH: AddEthereumChainParameter['nativeCurrency'] = {
    name: 'Ether',
    symbol: 'ETH',
    decimals: 18,
};

interface BasicChainInformation {
    urls: string[];
    name: string;
}

interface ExtendedChainInformation extends BasicChainInformation {
    nativeCurrency: AddEthereumChainParameter['nativeCurrency'];
    blockExplorerUrls: AddEthereumChainParameter['blockExplorerUrls'];
}

function isExtendedChainInformation(
    chainInformation: BasicChainInformation | ExtendedChainInformation
): chainInformation is ExtendedChainInformation {
    return !!(chainInformation as ExtendedChainInformation).nativeCurrency;
}

export function getAddChainParameters(chainId: number): AddEthereumChainParameter | number {
    const chainInformation = CHAINS[chainId];
    if (isExtendedChainInformation(chainInformation)) {
        return {
            chainId,
            chainName: chainInformation.name,
            nativeCurrency: chainInformation.nativeCurrency,
            rpcUrls: chainInformation.urls,
            blockExplorerUrls: chainInformation.blockExplorerUrls,
        };
    } else {
        return chainId;
    }
}


type ChainConfig = { [chainId: number]: BasicChainInformation | ExtendedChainInformation };

export const MAINNET_CHAINS: ChainConfig = {
    1: {
        urls: ['https://cloudflare-eth.com'],
        name: 'Mainnet',
    },
};

export const TESTNET_CHAINS: ChainConfig = {
    11155111: {
        urls: ['https://rpc.sepolia.dev'],
        name: 'Sepolia',
        nativeCurrency: ETH,
    },
};

export const CHAINS: ChainConfig = {
    ...MAINNET_CHAINS,
    ...TESTNET_CHAINS,
};

export const URLS: { [chainId: number]: string[] } = Object.keys(CHAINS).reduce<{
    [chainId: number]: string[];
}>((accumulator, chainId) => {
    const validURLs: string[] = CHAINS[Number(chainId)].urls;

    if (validURLs.length) {
        accumulator[Number(chainId)] = validURLs;
    }

    return accumulator;
}, {});
