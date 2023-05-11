import { createBoard } from '@wixc3/react-board';
import { MetamaskConnect } from '../../../components/metamask-connect/metamask-connect';

export default createBoard({
    name: 'MetamaskConnect',
    Board: () => <MetamaskConnect />
});
