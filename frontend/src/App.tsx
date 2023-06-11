import { useWeb3React, Web3ReactHooks, Web3ReactProvider } from '@web3-react/core';
import type { MetaMask } from '@web3-react/metamask';
import { ethers } from 'ethers';
import { Web3Provider } from '@ethersproject/providers';
import { Web3Storage, File } from 'web3.storage';
import { hooks as metaMaskHooks, metaMask } from './connectors/metamask';
import { NavBar } from './components/nav-bar/nav-bar';
import { TowerCard, TowerData } from './components/tower-card/tower-card';
import { Icon } from '@blueprintjs/core';
import App_module from './App.module.scss';
import { useEffect, useState } from 'react';
import { Buffer } from 'buffer';
import abi from './abi.json';

const connectors: [MetaMask, Web3ReactHooks][] = [[metaMask, metaMaskHooks]];
const WEB3_STORAGE_KEY = process.env.REACT_APP_WEB3_STORAGE_KEY || '?';

interface TowerSubmission {
    card1: TowerData;
    card2: TowerData;
    card3: TowerData;
    card4: TowerData;
    card5: TowerData;
    card6: TowerData;
    card7: TowerData;
}

function Submit(data: TowerSubmission) {
    const { connector } = useWeb3React();
    const { isActive, chainId, account, provider } = useWeb3React();

    async function storeCard(card: TowerData) {
        const client = new Web3Storage({ token: WEB3_STORAGE_KEY });
        const buffer = Buffer.from(JSON.stringify(card));
        const file = [
            new File(['contents-of-file-1'], 'plain-utf8.txt'),
            new File([buffer], 'card.json', { type: 'application/json' }),
        ];
        const cid = await client.put(file);
        console.log('stored files with cid:', cid);
        const built_card = {
            id: cid,
            teir: card.tier,
            priority: card.priority,
            operator: card.operator,
            data1: card.data1,
            data2: card.data2,
            data3: card.data3,
        };
        return built_card;
    }

    async function buildData(data: TowerSubmission) {
        // console.log(isActive, chainId, account, provider);
        // console.log(data);
        const client = new Web3Storage({ token: WEB3_STORAGE_KEY });
        const nft = {
            name: 'PrimeCrusaders Tower',
            description: 'Used in the PrimeCrusaders TD game',
            properties: {
                card1: await storeCard(data.card1),
                card2: await storeCard(data.card2),
                card3: await storeCard(data.card3),
                card4: await storeCard(data.card4),
                card5: await storeCard(data.card5),
                card6: await storeCard(data.card6),
                card7: await storeCard(data.card7),
            },
        };
        const buffer = Buffer.from(JSON.stringify(nft));
        const file = [
            new File(['contents-of-file-1'], 'plain-utf8.txt'),
            new File([buffer], 'tower.json', { type: 'application/json' }),
        ];
        const cid = await client.put(file);
        console.log('tower cid:', cid);
        console.log('nft: ');
        console.log(nft);
        return cid;
    }

    async function joinQueue(data: TowerSubmission) {
        if (!isActive) {
            return;
        }
        const cid = await buildData(data);

        const eth_provider = new ethers.BrowserProvider(connector.provider);
        const eth_signer = await eth_provider.getSigner();
        const contractAddress = '0x9f6105FB3b13F99F074cDC0CDDbc8222a9cc5129';
        const contract = new ethers.Contract(contractAddress, abi.abi, eth_signer);

        const tx = await contract.joinQueue(cid);
        await tx.wait();
        const status = contract.queue_status();
        console.log(status);
    }

    return (
        <button className={App_module['minting-buttons']} onClick={() => joinQueue(data)}>
            <Icon icon="archive" size={18} />
        </button>
    );
}

export default function App() {
    const [card11, setcard11] = useState({
        tier: 1,
        priority: 1,
        operator: 0,
        data1: 2,
        data2: 11,
        data3: 5,
    });

    const [card12, setcard12] = useState({
        tier: 1,
        priority: 2,
        operator: 1,
        data1: 2,
        data2: 11,
        data3: 5,
    });

    const [card21, setcard21] = useState({
        tier: 2,
        priority: 3,
        operator: 2,
        data1: 2,
        data2: 11,
        data3: 5,
    });

    const [card22, setcard22] = useState({
        tier: 2,
        priority: 4,
        operator: 3,
        data1: 2,
        data2: 11,
        data3: 5,
    });

    const [card23, setcard23] = useState({
        tier: 2,
        priority: 5,
        operator: 2,
        data1: 2,
        data2: 11,
        data3: 5,
    });

    const [card31, setcard31] = useState({
        tier: 3,
        priority: 6,
        operator: 1,
        data1: 2,
        data2: 11,
        data3: 5,
    });

    const [card32, setcard32] = useState({
        tier: 3,
        priority: 7,
        operator: 0,
        data1: 2,
        data2: 11,
        data3: 5,
    });

    const [tower, setTower] = useState({
        card1: card11,
        card2: card12,
        card3: card21,
        card4: card22,
        card5: card23,
        card6: card31,
        card7: card32,
    });

    useEffect(() => {
        setTower((prevData: TowerSubmission) => ({
            ...prevData,
            card1: card11,
            card2: card12,
            card3: card21,
            card4: card22,
            card5: card23,
            card6: card31,
            card7: card32,
        }));
    }, [card11, card12, card21, card22, card23, card31, card32]);

    return (
        <Web3ReactProvider connectors={connectors}>
            <span className={App_module.app}>
                <NavBar />
                <div className={App_module['card-row']}>
                    <TowerCard tower={card11} update={setcard11} />
                    <TowerCard tower={card12} update={setcard12} />
                </div>
                <div className={App_module['card-row']}>
                    <TowerCard tower={card21} update={setcard21} />
                    <TowerCard tower={card22} update={setcard22} />
                    <TowerCard tower={card23} update={setcard23} />
                </div>
                <div className={App_module['card-row']}>
                    <TowerCard tower={card31} update={setcard31} />
                    <TowerCard tower={card32} update={setcard32} />
                </div>
                <div className={App_module['minting-bar']}>
                    <button className={App_module['minting-buttons']}>
                        <Icon icon="refresh" size={18} />
                    </button>
                    <Submit {...tower} />
                </div>
            </span>
        </Web3ReactProvider>
    );
}
