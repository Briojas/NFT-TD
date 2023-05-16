import { createBoard } from '@wixc3/react-board';
import { Web3Button } from '../../../components/web-3-button/web-3-button';

import { hooks, metaMask } from '../../../connectors/metamask';
import { Dispatch, SetStateAction } from 'react';

const chainId = 11155111;
const accounts = ['0x709A77DfAAd078b257ec8D6d2Fd425727BDb1722'];
const isActivating = false;
const isActive = false;
const provider = undefined;
const ENSNames = [undefined];
const error = undefined;
const setError = null as unknown as Dispatch<SetStateAction<undefined>>;
const testHasMetamask = true;

export default createBoard({
    name: 'Web3Button',
    Board: () => (
        <Web3Button
            connector={metaMask}
            activeChainId={chainId}
            isActivating={isActivating}
            isActive={isActive}
            error={error}
            setError={setError}
            accounts={accounts}
            provider={provider}
            ENSNames={ENSNames}
            testHasMetamask={testHasMetamask}
        />
    ),
});
