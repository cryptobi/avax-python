# avax-python : Python tools for the exploration of the Avalanche AVAX network.
#
# Find tutorials and use cases at https://crypto.bi

"""

Copyright (C) 2021 - crypto.bi

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

Help support this Open Source project!
Donations address: X-avax1qr6yzjykcjmeflztsgv6y88dl0xnlel3chs3r4
Thank you!

"""

# --#--#--


from typing import List, Set
from avaxpython.ids.ID import ID
from avaxpython.snow.engine.avalanche.transitive import Transitive as AVMTransitive
from avaxpython.snow.engine.snowman.transitive import Transitive as SnowTransitive
from avaxpython.chains.subnet import Subnet, subnet
from avaxpython.snow.engine.avalanche.vertex.vm import DAGVM
from avaxpython.snow.engine.avalanche.config.config import Config as AvalancheConfig
from avaxpython.snow.engine.snowman.block.vm import ChainVM
from avaxpython.snow.networking.router.handler import Handler
from avaxpython.snow.context import Context
from avaxpython.utils.constants import application
from avaxpython.ids.aliases import Aliaser
from avaxpython.chains import chain_configs
from avaxpython.chains.chain_configs import AVAXAssetID, ConsensusDispatcher, DecisionDispatcher, x_chain_id
from avaxpython.chains.chain import chain
from avaxpython.chains.chain_parameters import ChainParameters
from avaxpython.chains.manager_config import ManagerConfig
from avaxpython.snow.engine.avalanche.bootstrap.config import Config as BootstrapConfig
from avaxpython.snow.engine.common.config import Config as CommonConfig


class Manager:

    def __init__(self):
        self.chains = {}
        self.subnets = {}
        self.config = ManagerConfig()
        self.aliaser = Aliaser()

    def Router(self):
        pass

    def CreateChain(self, chain_parameters):
        """Create a chain in the future"""
        pass
    
    def ForceCreateChain(self, chain_parameters):
        """Create a chain now"""
        
        if chain_parameters.SubnetID in self.subnets:
            sb = self.subnets[chain_parameters.SubnetID]
        else:
            sb = subnet()
            self.subnets[chain_parameters.SubnetID] = sb

        sb.addChain(chain_parameters.ID)

        chain = self.buildChain(chain_parameters, sb)
        self.chains[chain_parameters.ID] = chain.Handler

        # Until we have proper dynamic chain creation, load the main chains
        # from static config.

        chain_configs.NodeID = chain_parameters.NodeID
        chain_configs.InitChains()
        
        for chain_id_str in chain_configs.chains:
            chain = chain_configs.chains[chain_id_str]
            self.chains[str(chain_parameters.ID)] = chain
            self.config.Router.AddChain(chain.Handler)


    def buildChain(self, chain_parameters: ChainParameters, sb: Subnet):
        
        vmID = self.config.VMManager.Lookup(chain_parameters.VMAlias)        
        primaryAlias = self.aliaser.PrimaryAlias(chain_parameters.ID)
        new_chain : chain = None

        chain_configs.AVAXAssetID = self.config.AVAXAssetID
        chain_configs.x_chain_id = self.config.x_chain_id
        chain_configs.DecisionDispatcher = self.config.DecisionEvents
        chain_configs.ConsensusDispatcher = self.config.ConsensusEvents

        ctx = Context(
            NetworkID =  self.config.NetworkID,
            SubnetID = chain_parameters.SubnetID,
            chain_id = chain_parameters.ID,
            NodeID = self.config.NodeID,
            x_chain_id = self.config.x_chain_id,
            AVAXAssetID = self.config.AVAXAssetID,
            Log = None,
            DecisionDispatcher = self.config.DecisionEvents,
            ConsensusDispatcher = self.config.ConsensusEvents,
            Keystore = None,
            SharedMemory = None,
            BCLookup = self,
            SNLookup = self,
            Namespace = f"{application.PlatformName}_{primaryAlias}_vm",
            Metrics = None,
            EpochFirstTransition = self.config.EpochFirstTransition,
            EpochDuration = self.config.EpochDuration,
        )

        fxs = []

        vmFactory = self.config.VMManager.GetVMFactory(vmID)
        vm = vmFactory.New(ctx)
        consensusParams = self.config.ConsensusParams
        vdrs = self.config.Validators.GetValidators(chain_parameters.SubnetID)

        beacons = vdrs
        if chain_parameters.CustomBeacons:
            beacons = chain_parameters.CustomBeacons	

        if isinstance(vm, DAGVM):
            
            new_chain = self.createAvalancheChain(
                ctx,
                chain_parameters,
                vdrs,
                beacons,
                vm,
                fxs,
                consensusParams,
                0,
                sb,
            )
            
        elif isinstance(vm, ChainVM):
            new_chain = self.createSnowmanChain(
                ctx,
                chain_parameters,
                vdrs,
                beacons,
                vm,
                fxs,
                consensusParams,
                0,
                sb,
            )
            
        else:
            raise Exception("the vm should have type avalanche.DAGVM or snowman.ChainVM. Chain not created")
        

        self.config.Router.AddChain(new_chain.Handler)

        return new_chain


    def AddRegistrant(self, Registrant):
        """Add a registrant [r]. Every time a chain is created, [r].RegisterChain([new chain]) is called"""
        pass
    
    def Lookup(self, alias: str) -> ID:
        """Given an alias, return the ID of the chain associated with that alias"""
        pass

    def LookupVM(self, alias: str) -> ID:
        """Given an alias, return the ID of the VM associated with that alias"""
        pass
    
    def Aliases(self, a_id: ID) -> List[str]:
        """Return the aliases associated with a chain"""
        pass
    
    def Alias(self, a_id: ID, alias: str):
        """Add an alias to a chain"""
        pass

    def SubnetID(self, chaina_ID: ID) -> ID:
        """Returns the ID of the subnet that is validating the provided chain"""
        pass 

    def IsBootstrapped(self, a_id: ID) -> bool:
        """Returns true iff the chain with the given ID exists and is finished bootstrapping"""

    def Shutdown(self):
        pass

    def createAvalancheChain(self, ctx, chain_params, validators, beacons, vm, fxs, consensusParams, bootstrapWeight, sb):
        engine = AVMTransitive(vm, ctx)
        engine.Initialize(AvalancheConfig(
		ConfigP = BootstrapConfig(
			CConfig = CommonConfig(
				Ctx =                       ctx,
				Validators=                validators,
				Beacons=                   beacons,
				SampleK=                   sampleK,
				StartupAlpha=              (3*bootstrapWeight + 3) / 4,
				Alpha=                     bootstrapWeight/2 + 1, # must be > 50%
				Sender=                    sender,
				Subnet=                    sb,
				Delay=                     delay,
				RetryBootstrap=            m.RetryBootstrap,
				RetryBootstrapMaxAttempts= m.RetryBootstrapMaxAttempts,
            ),
			VtxBlocked= vtxBlocker,
			TxBlocked=  txBlocker,
			Manager=    vtxManager,
			VM=         vm
        ),
		Params=    consensusParams,
		Consensus = avcon.Topological(),
        ))
        genesisData = chain_params.GenesisData
        
        handler = Handler(ctx=ctx, engine=engine)        
        handler.Initialize(engine, validators, None, self.config.MaxPendingMsgs, self.config.MaxNonStakerPendingMsgs, self.config.StakerMSGPortion, self.config.StakerCPUPortion, f"{consensusParams.Namespace}_handler", consensusParams.Metrics, None)

        chainAlias = self.PrimaryAlias(ctx.chain_id)
        return chain(
            name = chainAlias,
            engine = engine,
            handler = handler,
            vm = vm,
            ctx = ctx,
            params = chain_params
        )

    def createSnowmanChain(self, ctx, chain_params, validators, beacons, vm, fxs, consensusParams, bootstrapWeight, sb):        
        engine = SnowTransitive(vm, ctx)
        handler = Handler(ctx=ctx, engine=engine)
        genesisData = chain_params.GenesisData
        handler.Initialize(engine, validators, None, self.config.MaxPendingMsgs, self.config.MaxNonStakerPendingMsgs, self.config.StakerMSGPortion, self.config.StakerCPUPortion, f"{consensusParams.Namespace}_handler", consensusParams.Metrics, None)
        
        chainAlias = self.aliaser.PrimaryAlias(ctx.chain_id)

        return chain(
            name = chainAlias,
            engine = engine,
            handler = handler,
            vm = vm,
            ctx = ctx,
            beacons = beacons,
            params = chain_params
        )



