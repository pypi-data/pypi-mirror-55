from ..kernel import core
from ..kernel.core import VSkillModifier as V
from ..character import characterKernel as ck
from functools import partial
from ..status.ability import Ability_tool
from . import globalSkill
from .jobbranch import thieves
#TODO : 5차 신스킬 적용

# TODO: 왜 레투다는 5차값이 1,1인데 레투다 패시브는 2,2일까?

class JobGenerator(ck.JobGenerator):
    def __init__(self):
        super(JobGenerator, self).__init__()
        self.buffrem = False
        self.jobtype = "luk"
        self.ability_list = Ability_tool.get_ability_set('boss_pdamage', 'crit', 'buff_rem')
        self.preEmptiveSkills = 1

    def get_modifier_optimization_hint(self):
        return core.CharacterModifier(armor_ignore = 86)

    def get_passive_skill_list(self):
        Karma = core.InformedCharacterModifier("카르마", att = 30)
        PhisicalTraining = core.InformedCharacterModifier("피지컬 트레이닝", stat_main = 30, stat_sub = 30)
        
        SornsEffect = core.InformedCharacterModifier("쏜즈 이펙트", att = 30)
        DualBladeExpert = core.InformedCharacterModifier("이도류 엑스퍼트", att = 30, pdamage_indep = 20)
        Sharpness = core.InformedCharacterModifier("샤프니스", crit = 35, crit_damage = 13)
        ReadyToDiePassive = thieves.ReadyToDiePassiveWrapper(self.vEhc, 2, 2)
        
        return [Karma, PhisicalTraining, SornsEffect, DualBladeExpert, Sharpness,
                            ReadyToDiePassive]

    def get_not_implied_skill_list(self):
        WeaponConstant = core.InformedCharacterModifier("무기상수", pdamage_indep = 30)
        Mastery = core.InformedCharacterModifier("숙련도", pdamage_indep = -5)    #오더스 기본적용!   
        return [WeaponConstant, Mastery]

    def generate(self, vEhc, chtr : ck.AbstractCharacter, combat : bool = False):
        '''
        하이퍼 : 팬텀 블로우 - 리인포스, 이그노어 가드, 보너스 어택
        블레이드 퓨리 - 리인포스, 엑스트라 타겟
        
        미러이미징을 뎀뻥으로 계산.(:= 맥뎀 누수계산에 오류가 있을 수 있음)
        아수라 41타
        블레이드 토네이도 3타
        카르마 퓨리 사용
        
        코어 16개 유효 : 팬블 / 아수라 / 퓨리 -- 써든레이드 / 어센션 / 히든블레이드
        '''

        
        #Buff skills
        Booster = core.BuffSkill("부스터", 0, 180000, rem = True).wrap(core.BuffSkillWrapper)
        MirrorImaging = core.BuffSkill("미러 이미징", 0, 200000, rem = True, pdamage_indep = 70).wrap(core.BuffSkillWrapper)
        
        DarkSight = core.BuffSkill("다크 사이트", 0, 1, cooltime = -1, pdamage_indep = 20 + 10 + int(0.2*vEhc.getV(3,3))).wrap(core.BuffSkillWrapper)
        
        PhantomBlow = core.DamageSkill("팬텀 블로우", 540, 315, 6+1, modifier = core.CharacterModifier(armor_ignore = 30+20, pdamage = 20)).setV(vEhc, 0, 2, False).wrap(core.DamageSkillWrapper)
        SuddenRaid = core.DamageSkill("써든 레이드", 900, 1150, 3, cooltime = 30000).setV(vEhc, 2, 2, False).wrap(core.DamageSkillWrapper)    #파컷의 남은 쿨타임 20% 감소
        SuddenRaidDOT = core.DotSkill("써든 레이드(도트)", 210/1.7, 10000).wrap(core.SummonSkillWrapper)
        
        FinalCut = core.DamageSkill("파이널 컷", 870, 2000, 1, cooltime = 90000).wrap(core.DamageSkillWrapper)
        FinalCutBuff = core.BuffSkill("파이널 컷(버프)", 0, 60000, rem = True, pdamage_indep = 40).wrap(core.BuffSkillWrapper)
        
        EpicAdventure = core.BuffSkill("에픽 어드벤처", 0, 60*1000, cooltime = 120 * 1000, pdamage = 10).wrap(core.BuffSkillWrapper)
        
        FlashBang = core.DamageSkill("플래시 뱅", 600, 250, 1, cooltime = 60000).wrap(core.DamageSkillWrapper)  #임의 딜레이.
        FlashBangDebuff = core.BuffSkill("플래시 뱅(디버프)", 0, 50000/2, cooltime = -1, pdamage = 10 * 0.9).wrap(core.BuffSkillWrapper)
        Venom = core.DotSkill("페이탈 베놈", 160*3/1.7, 8000).wrap(core.SummonSkillWrapper)
        
        HiddenBladeBuff = core.BuffSkill("히든 블레이드(버프)", 0, 60000, cooltime = 90000, pdamage = 10).wrap(core.BuffSkillWrapper)
        HiddenBlade = core.DamageSkill("히든 블레이드", 0, 140 / 1.7, 2).setV(vEhc, 5, 2, True).wrap(core.DamageSkillWrapper)    #미러 이미징에 의해 추가타 2개, 최종뎀 1.7배 무시
        
        Asura = core.DamageSkill("아수라", 0, 0, 0, cooltime = 60000).wrap(core.DamageSkillWrapper)
        AsuraTick = core.DamageSkill("아수라(틱)", 300, 420, 4, modifier =core.CharacterModifier(armor_ignore = 100)).setV(vEhc, 1, 2, False).wrap(core.DamageSkillWrapper)  #41타
        
        UltimateDarksight = core.BuffSkill("얼티밋 다크사이트", 750, 30000, red = True, cooltime = (220-vEhc.getV(3,3))*1000).isV(vEhc,3,3).wrap(core.BuffSkillWrapper)
        ReadyToDie = thieves.ReadyToDieWrapper(vEhc,1,1)
        
        BladeStorm = core.DamageSkill("블레이드 스톰", 660, 580+23*vEhc.getV(0,0), 7, red = True, cooltime = 90000, modifier = core.CharacterModifier(armor_ignore = 100)).isV(vEhc,0,0).wrap(core.DamageSkillWrapper)
        BladeStormTick = core.DamageSkill("블레이드 스톰(틱)", 210, 350+10*vEhc.getV(0,0), 5, modifier = core.CharacterModifier(armor_ignore = 100)).isV(vEhc,0,0).wrap(core.DamageSkillWrapper)  #10000/210 타
        
        KarmaFury = core.DamageSkill("카르마 퓨리", 990, 750+30*vEhc.getV(6,6), 7 * 3, red = True, cooltime = 10000, modifier = core.CharacterModifier(armor_ignore = 30)).isV(vEhc,6,6).wrap(core.DamageSkillWrapper)
        BladeTornado = core.DamageSkill("블레이드 토네이도", 720, 600+24*vEhc.getV(2,2), 7, cooltime = 12000, modifier = core.CharacterModifier(armor_ignore = 100)).isV(vEhc,2,2).wrap(core.DamageSkillWrapper)
        #BladeTornadoFront = core.DamageSkill("블레이드 토네이도(전방)", 0, 600+24*vEhc.getV(2,2), 6, modifier = core.CharacterModifier(armor_ignore = 100)).isV(vEhc,2,2).wrap(core.DamageSkillWrapper)   #보통 1타
        BladeTornadoSummon = core.SummonSkill("블레이드 토네이도(소환)", 0, 540, 450+18*vEhc.getV(2,2), 6 * 3, 2000, cooltime=-1, modifier = core.CharacterModifier(armor_ignore = 100)).isV(vEhc,2,2).wrap(core.SummonSkillWrapper) #임의 딜레이, 미사용
        
        ######   Skill Wrapper   ######
    
        SuddenRaid.onAfter(SuddenRaidDOT)
        FinalCut.onAfter(FinalCutBuff)
        
        HiddenBladeOpt = core.OptionalElement(HiddenBladeBuff.is_active, HiddenBlade)
        
        FlashBang.onAfter(FlashBangDebuff)
        for sk in [FinalCut, PhantomBlow, SuddenRaid, FlashBang, AsuraTick, BladeStorm, BladeStormTick, BladeTornado, BladeTornadoSummon]:
            sk.onAfter(HiddenBladeOpt)
            
        for sk in [PhantomBlow, AsuraTick, BladeStormTick]:
            sk.onAfter(Venom)
        
        Asura.onAfter(core.RepeatElement(AsuraTick, int((10+3)*1000/300)))
        BladeStorm.onAfter(core.RepeatElement(BladeStormTick, int((10000+3000)/210)))
        #BladeTornado.onAfter(BladeTornadoFront)
        BladeTornado.onAfter(BladeTornadoSummon)
        
        return(PhantomBlow,
                [globalSkill.maple_heros(chtr.level), globalSkill.useful_sharp_eyes(),
                    Booster, MirrorImaging, DarkSight, FinalCutBuff, EpicAdventure, FlashBangDebuff, HiddenBladeBuff, UltimateDarksight, ReadyToDie,
                    globalSkill.soul_contract()] +\
                [FinalCut, FlashBang, Asura, BladeStorm, BladeTornado, SuddenRaid, KarmaFury] +\
                [SuddenRaidDOT, Venom, BladeTornadoSummon] +\
                [] +\
                [PhantomBlow])