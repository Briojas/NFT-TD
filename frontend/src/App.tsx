import Wrapper from './components/web-3-button/wrapper';
import { NavBar } from './components/nav-bar/nav-bar';

export default function App() {
    return (
        <>
            <Wrapper />
            <div
                style={{
                    display: 'flex',
                    flexFlow: 'row nowrap',
                    fontFamily: 'sans-serif',
                    alignItems: 'stretch',
                    justifyItems: 'stretch',
                }}
            >
                <NavBar />
            </div>
        </>
    );
}
